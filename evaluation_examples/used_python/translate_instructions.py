import json
import os
import asyncio
from openai import OpenAI

def generate_completion(prompt):
    """
    Generate text completion using OpenAI API.
    
    Args:
        prompt (str): The prompt text to generate completion for.
    
    Returns:
        str: The generated completion text.
    """
    # Specify the API key
    api_key = os.getenv("OPENAI_API_KEY_GENIAC")
    client = OpenAI()
    client.api_key = api_key

    # Initialize the OpenAI object
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ]
    )
    completion_text = completion.choices[0].message.content.strip()
    return completion_text

async def translate_gpt(english_text):
    """
    Translate English text to Japanese text.
    Args:
        english_text (str): English text to translate.
    Returns:
        str: Japanese translation of the English text.
    """
    # Specify the language code for Japanese
    prompt = """
    Translate the following English text into natural Japanese.

    For polite expressions such as “Please” or “would like to,” use honorific language. 
    Otherwise, use imperative or declarative forms.
    Output only the translation of the English text, without any additional information.
    Text:
    """.strip() + english_text
    # Translate the English text to Japanese
    japanese_text = generate_completion(prompt)
    return japanese_text

async def process_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for category, files in data.items():
        if category == 'Windows':
            continue
        for filename, instructions in files.items():
            if isinstance(instructions, dict) and instructions.get('instruction_jp') is None:
                instruction_en = instructions.get('instruction_en')
                if instruction_en:
                    translated_instruction = await translate_gpt(instruction_en)
                    instructions['instruction_jp'] = translated_instruction
                    print(f"Updated file: {filename}")

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def main():
    json_file_path = '/Users/shojibumbu/dev/OSWorld/evaluation_examples/instructions_translated.json'
    await process_json_file(json_file_path)

if __name__ == "__main__":
    asyncio.run(main())
