import os
import json

def update_instructions():
    # 翻訳データのファイルパス（適宜パスを変更してください）
    translations_path = 'instructions_translated.json'
    # JSON ファイル群があるルートディレクトリ
    examples_dir = 'examples_japanese'
    
    # 翻訳データ（JSON）を読み込む
    with open(translations_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    # examples_dir 以下のすべてのファイルを再帰的に探索する
    for root, dirs, files in os.walk(examples_dir):
        for file in files:
            if not file.endswith('.json'):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"ファイル読み込みエラー ({file_path}): {e}")
                continue

            # JSON内に "instruction" フィールドがなければスキップ
            if 'instruction' not in data:
                continue

            # 例:  relative_path = "chrome/a728a36e-8bf1-4bb6-9a03-ef039a5233f0.json" などになる
            rel_path = os.path.relpath(file_path, examples_dir)
            path_parts = rel_path.split(os.sep)

            translation_file_key = file
            if translation_file_key.startswith("J_"):
                translation_file_key = translation_file_key[2:]

            # ルート直下の JSON ファイルの場合（例: "J_template.json"）
            if len(path_parts) == 1:
                # "J_template.json" → "template.json" に変換（必要に応じて調整）
                if translation_file_key in translations:
                    new_instruction = translations[translation_file_key].get('instruction_jp')
                    if new_instruction and data['instruction'] != new_instruction:
                        data['instruction'] = new_instruction
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        print(f'更新しました: {file_path}')
                else:
                    print(f"翻訳データが見つかりませんでした（ルート）: {translation_file_key}")

            # サブディレクトリ内の JSON ファイルの場合
            else:
                # Windows ディレクトリの場合は、さらにサブフォルダが存在するので特別処理
                if path_parts[0] == "Windows":
                    # 例: path_parts = ["Windows", "excel", "example_excel.json"]
                    if len(path_parts) < 3:
                        print(f"想定外のパス構造 (Windows): {rel_path}")
                        continue
                    subfolder = path_parts[1]  # excel, multi_app, word, ppt など
                    if ("Windows" in translations and 
                        subfolder in translations["Windows"] and 
                        translation_file_key in translations["Windows"][subfolder]):
                        
                        new_instruction = translations["Windows"][subfolder][translation_file_key].get("instruction_jp")
                        if new_instruction and data["instruction"] != new_instruction:
                            data["instruction"] = new_instruction
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                            print(f'更新しました: {file_path}')
                    else:
                        print(f"翻訳データが見つかりませんでした (Windows): {rel_path}")
                else:
                    # その他のサブディレクトリ（例: chrome, libreoffice_calc, vlc など）
                    folder = path_parts[0]
                    if folder in translations and translation_file_key in translations[folder]:
                        new_instruction = translations[folder][translation_file_key].get("instruction_jp")
                        if new_instruction and data["instruction"] != new_instruction:
                            data["instruction"] = new_instruction
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                            print(f'更新しました: {file_path}')
                    else:
                        print(f"翻訳データが見つかりませんでした: {rel_path}")

if __name__ == "__main__":
    update_instructions()
