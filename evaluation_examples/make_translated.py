import json

# ファイルを読み込む
with open('instructions.json', 'r', encoding='utf-8') as instructions_file:
    instructions_data = json.load(instructions_file)

with open('translations.json', 'r', encoding='utf-8') as translations_file:
    translations_data = json.load(translations_file)

# translationsの要素をinstructionsに追加
for filename, translations in translations_data.items():
    for folder, subfolders in instructions_data.items():
        if folder == 'Windows':
            for subfolder, files in subfolders.items():
                if filename in files:
                    instruction_en = files[filename].get('instruction_en')
                    if instruction_en in translations:
                        files[filename]['instruction_jp'] = translations[translations.index(instruction_en) + 1]
        else:
            if filename in subfolders:
                instruction_en = subfolders[filename].get('instruction_en')
                if instruction_en in translations:
                    subfolders[filename]['instruction_jp'] = translations[translations.index(instruction_en) + 1]

# 更新されたinstructionsを保存
with open('instructions_translated.json', 'w', encoding='utf-8') as instructions_file:
    json.dump(instructions_data, instructions_file, ensure_ascii=False, indent=4)

print("instructions.jsonが更新されました。")