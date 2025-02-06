import os
import json

# translations.jsonのパス
translations_path = '/Users/shojibumbu/dev/OSWorld/evaluation_examples/translations.json'

# examplesフォルダのパス
examples_path = '/Users/shojibumbu/dev/OSWorld/evaluation_examples/examples/'

# translations.jsonを読み込む
with open(translations_path, 'r', encoding='utf-8') as f:
    translations = json.load(f)

# examplesフォルダ内の各JSONファイルを処理
for root, dirs, files in os.walk(examples_path):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # JSONファイルに"instruction"フィールドがあるか確認
            if 'instruction' in data:
                # translations.jsonに対応するキーがあるか確認
                if file in translations:
                    # 両者の"instruction"が異なる場合、translations.jsonのものに書き換える
                    if data['instruction'] != translations[file][0]:
                        #data['instruction'] = translations[file][0]
                        # 修正後のJSONファイルを上書き保存
                        #with open(file_path, 'w', encoding='utf-8') as f:
                        #    json.dump(data, f, ensure_ascii=False, indent=4)
                        print(f'different {file}')