import os
import json

def create_dict_from_examples(root_dir):
    result = {}

    for root, dirs, files in os.walk(root_dir):
        # フォルダの階層を取得
        folder_hierarchy = root.replace(root_dir, '').strip(os.sep).split(os.sep)
        current_dict = result

        # フォルダの階層に従って辞書を作成
        for folder in folder_hierarchy:
            if folder:
                current_dict = current_dict.setdefault(folder, {})

        # ファイルを辞書に追加
        for file in files:
            if file.endswith('.json'):  # .jsonファイルを対象とする
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    example = json.load(f)
                if 'instruction' in example:
                    current_dict[file] = {"instruction_en": example['instruction'], "instruction_jp": None}

    return result

# examplesディレクトリから辞書を作成
examples_dir = 'examples'
instructions_dict = create_dict_from_examples(examples_dir)

# 辞書をJSONファイルとして保存
with open('instructions.json', 'w', encoding='utf-8') as json_file:
    json.dump(instructions_dict, json_file, ensure_ascii=False, indent=4)

print("instructions.jsonが作成されました。")