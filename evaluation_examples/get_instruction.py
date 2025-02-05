import json
import os
import asyncio

from openai import OpenAI
from googletrans import Translator


def get_instruction(json_file_path):
    """
    Extract the 'instruction' field from a specific JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file.
    
    Returns:
        str: The instruction from the JSON file.
    """
    try:
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Extract the 'instruction' field
        instruction = data.get('instruction', None)
        if instruction:
            return instruction
        else:
            return "No 'instruction' field found in the JSON file."
    except FileNotFoundError:
        return f"File not found: {json_file_path}"
    except json.JSONDecodeError:
        return f"Error decoding JSON file: {json_file_path}"


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

def translate_en_to_jp(english_text):
    """
    Translate English text to Japanese text.
    Args:
        english_text (str): English text to translate.
    Returns:
        str: Japanese translation of the English text.
    """
    # Specify the language code for Japanese
    prompt = "Translate the following English text to Japanese:\n\n" + english_text
    # Translate the English text to Japanese
    japanese_text = generate_completion(prompt)
    return japanese_text

async def translate_text(text):
    translator = Translator()
    translation = await translator.translate(text, src='en', dest='ja')
    return translation.text

async def translate_onefile():
    # Specify the path to the JSON file
    json_file_path = "evaluation_examples/examples/Windows/excel/3aaa4e37-dc91-482e-99af-132a612d40f3.json"

    # Get the instruction
    instruction = get_instruction(json_file_path)
    instruction_jp = await translate_text(instruction)

    # Print the instruction
    print("Instruction:", instruction, "\n"
        "Japanese Translation:", instruction_jp)

async def process_json_files(input_dir, output_dir, json_file):
    translations = []

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_dir, 'J_' + os.path.relpath(input_file_path, input_dir))

                instruction = get_instruction(input_file_path)
                if instruction.startswith("File not found") or instruction.startswith("Error decoding"):
                    continue

                translated_instruction = await translate_text(instruction)
                translations.append([instruction, translated_instruction])
                
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['instruction'] = translated_instruction

                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)


async def main():
    input_dir = 'evaluation_examples/examples'
    output_dir = 'evaluation_examples/examples_japanese'
    json_file = 'translations.json'

    await process_json_files(input_dir, output_dir, json_file)

if __name__ == "__main__":
    asyncio.run(main())
