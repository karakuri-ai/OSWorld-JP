import os
import json
import re
from collections import defaultdict

# フォルダ名の変換マッピング
FOLDER_NAME_MAPPING = {
    "libreoffice_calc": "excel",
    "libreoffice_impress": "ppt",
    "libreoffice_writer": "word"
    # multi_app関連のマッピングを削除
}

# メインディレクトリパス
BASE_DIR = "/Users/shojibumbu/dev/osworld/evaluation_examples"

def get_json_files(dir_path):
    """指定したディレクトリ内のすべてのJSONファイルを取得する"""
    all_files = []
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                rel_path = os.path.relpath(root, BASE_DIR)
                all_files.append(os.path.join(rel_path, file))
    
    return all_files

def extract_uuid_from_filename(filename):
    """ファイル名からUUIDを抽出する"""
    uuid_pattern = r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    match = re.search(uuid_pattern, filename)
    if match:
        return match.group(1)
    return None

def is_windows_path(path):
    """パスがWindows配下かどうかを判定する"""
    return 'Windows' in path

# multi_app関連の特別な関数を削除
# is_multi_app_path関数を削除
# get_normalized_folder_name関数を削除

def generate_non_windows_filenames():
    """Windows以外のファイルに新しい名前を生成し、UUIDと新しいファイル名のマッピングを返す"""
    examples_dir = os.path.join(BASE_DIR, "examples")
    examples_files = get_json_files(examples_dir)
    
    # フォルダごとのカウンター
    folder_counters = defaultdict(int)
    filename_mapping = {}
    uuid_to_new_name = defaultdict(dict)  # フォルダごとにUUIDマッピングを管理
    
    # Windows以外のファイルをフィルタリングしてソート
    non_windows_files = [f for f in examples_files if not is_windows_path(f)]
    
    # ファイル名をソートして処理順序を一定にする
    for file_path in sorted(non_windows_files):
        filename = os.path.basename(file_path)
        file_uuid = extract_uuid_from_filename(filename)
        
        dir_path = os.path.dirname(file_path)
        folder_name = os.path.basename(dir_path)
        
        # multi_app関連の特別処理を削除
        
        # フォルダ名に基づいて新しいアプリ名を決定
        if folder_name in FOLDER_NAME_MAPPING:
            app_name = FOLDER_NAME_MAPPING[folder_name]
        else:
            app_name = folder_name
        
        # フォルダごとにカウンターを増加
        folder_counters[folder_name] += 1
        counter = folder_counters[folder_name]
        
        # 新しいファイル名を生成
        new_filename = f"{app_name}_{counter:02d}.json"
        
        # 元のパスと新しいパスのマッピングを保存
        new_file_path = os.path.join(dir_path, new_filename)
        filename_mapping[new_file_path] = file_path
        
        # UUIDと新しいファイル名のマッピングを保存（フォルダごとに）
        if file_uuid:
            uuid_to_new_name[folder_name][file_uuid] = new_filename
            
            # multi_apps/multi_app間の相互参照設定を削除
            
            # グローバルなマッピングは保持
            if 'global' not in uuid_to_new_name:
                uuid_to_new_name['global'] = {}
            uuid_to_new_name['global'][file_uuid] = new_filename
    
    return filename_mapping, uuid_to_new_name

def generate_windows_filenames(uuid_to_new_name):
    """Windowsフォルダ内のファイルに新しい名前を生成する"""
    examples_dir = os.path.join(BASE_DIR, "examples")
    examples_files = get_json_files(examples_dir)
    
    # フォルダごとのカウンター
    folder_counters = defaultdict(int)
    filename_mapping = {}
    
    # Windowsファイルをフィルタリングしてソート
    windows_files = [f for f in examples_files if is_windows_path(f)]
    
    for file_path in sorted(windows_files):
        filename = os.path.basename(file_path)
        file_uuid = extract_uuid_from_filename(filename)
        
        dir_path = os.path.dirname(file_path)
        folder_name = os.path.basename(dir_path)
        # Windows/multi_app フォルダの特殊処理を削除
        if 'multiapps' in folder_name:
            is_multi_app = True
        # 対応する非Windows版フォルダを探す
        non_windows_folder = folder_name
        
        # フォルダ名に基づいて新しいアプリ名を決定
        if folder_name in FOLDER_NAME_MAPPING:
            app_name = FOLDER_NAME_MAPPING[folder_name]
        else:
            app_name = folder_name
        
        # 新しいファイル名を決定
        new_filename = None
        
        if file_uuid:
            # 対応する非Windows版のファイルを探す
            if non_windows_folder in uuid_to_new_name and file_uuid in uuid_to_new_name[non_windows_folder]:
                base_name = uuid_to_new_name[non_windows_folder][file_uuid]
                base_app_name = base_name.split('_')[0]
                base_counter = base_name.split('_')[1].split('.')[0]
                new_filename = f"W_{base_app_name}_{base_counter}.json"
                if is_multi_app:
                    print(f"Multi-app file: {filename} -> {new_filename}")
            # フォールバック：グローバルマッピング
            elif 'global' in uuid_to_new_name and file_uuid in uuid_to_new_name['global']:
                base_name = uuid_to_new_name['global'][file_uuid]
                base_app_name = base_name.split('_')[0]
                base_counter = base_name.split('_')[1].split('.')[0]
                new_filename = f"W_{base_app_name}_{base_counter}.json"
        
        # UUIDが見つからなかった場合は新しい名前を生成
        if not file_uuid or new_filename is None:
            folder_counters[folder_name] += 1
            counter = folder_counters[folder_name]
            new_filename = f"W_{app_name}_{counter:02d}.json"
        
        # 元のパスと新しいパスのマッピングを保存
        new_file_path = os.path.join(dir_path, new_filename)
        filename_mapping[new_file_path] = file_path
    
    return filename_mapping

def generate_japanese_filenames(uuid_to_new_name):
    """examples_japanese ディレクトリ内のファイルに新しい名前を生成"""
    examples_jp_dir = os.path.join(BASE_DIR, "examples_japanese")
    examples_jp_files = get_json_files(examples_jp_dir)
    
    # フォルダごとのカウンター
    folder_counters = defaultdict(int)
    filename_mapping = {}
    
    # 日本語版のファイルをWindows配下とそれ以外に分ける
    non_windows_jp_files = [f for f in examples_jp_files if not is_windows_path(f)]
    windows_jp_files = [f for f in examples_jp_files if is_windows_path(f)]
    
    # 最初にWindows以外のファイルを処理
    for file_path in sorted(non_windows_jp_files):
        filename = os.path.basename(file_path)
        file_uuid = extract_uuid_from_filename(filename)
        
        dir_path = os.path.dirname(file_path)
        folder_name = os.path.basename(dir_path)
        
        # 新しいファイル名を決定
        new_filename = None
        if file_uuid:
            # 同じフォルダ内に同じUUIDを持つ英語版ファイルがあるかチェック
            if folder_name in uuid_to_new_name and file_uuid in uuid_to_new_name[folder_name]:
                new_base_filename = uuid_to_new_name[folder_name][file_uuid]
                new_filename = f"J_{new_base_filename}"
            # フォールバック：グローバルなUUIDマッピングを使用
            elif 'global' in uuid_to_new_name and file_uuid in uuid_to_new_name['global']:
                new_base_filename = uuid_to_new_name['global'][file_uuid]
                new_filename = f"J_{new_base_filename}"
        
        # UUIDが見つからなかった場合は新しい名前を生成
        if new_filename is None:
            if folder_name in FOLDER_NAME_MAPPING:
                app_name = FOLDER_NAME_MAPPING[folder_name]
            else:
                app_name = folder_name
            
            folder_counters[folder_name] += 1
            counter = folder_counters[folder_name]
            
            new_filename = f"J_{app_name}_{counter:02d}.json"
        
        # 元のパスと新しいパスのマッピングを保存
        new_file_path = os.path.join(dir_path, new_filename)
        filename_mapping[new_file_path] = file_path
    
    # 次にWindows配下のファイルを処理
    for file_path in sorted(windows_jp_files):
        filename = os.path.basename(file_path)
        file_uuid = extract_uuid_from_filename(filename)
        
        dir_path = os.path.dirname(file_path)
        folder_name = os.path.basename(dir_path)
        
        # Windows/multi_app フォルダの日本語版特殊処理を削除
        
        # 新しいファイル名を決定
        new_filename = None
        if file_uuid:
            # まずUUIDで直接検索
            if 'global' in uuid_to_new_name and file_uuid in uuid_to_new_name['global']:
                # グローバルマッピングから英語版の名前を取得
                new_base_filename = uuid_to_new_name['global'][file_uuid]
                base_app_name = new_base_filename.split('_')[0]
                base_counter = new_base_filename.split('_')[1].split('.')[0]
                new_filename = f"J_W_{base_app_name}_{base_counter}.json"
            elif folder_name in uuid_to_new_name and file_uuid in uuid_to_new_name[folder_name]:
                # 通常のフォルダ名でUUIDを検索
                new_base_filename = uuid_to_new_name[folder_name][file_uuid]
                base_app_name = new_base_filename.split('_')[0]
                base_counter = new_base_filename.split('_')[1].split('.')[0]
                new_filename = f"J_W_{base_app_name}_{base_counter}.json"
        
        # UUIDが見つからなかった場合は新しい名前を生成
        if new_filename is None:
            if folder_name in FOLDER_NAME_MAPPING:
                app_name = FOLDER_NAME_MAPPING[folder_name]
            else:
                app_name = folder_name
            
            folder_counters[folder_name] += 1
            counter = folder_counters[folder_name]
            
            new_filename = f"J_W_{app_name}_{counter:02d}.json"
        
        # 元のパスと新しいパスのマッピングを保存
        new_file_path = os.path.join(dir_path, new_filename)
        filename_mapping[new_file_path] = file_path
    
    return filename_mapping

def save_mapping_to_json(filename_mapping):
    """ファイル名のマッピングをJSONファイルに保存する"""
    folder_mapping = {}
    
    # ファイルパスをフォルダごとにグループ化し、ファイル名だけを抽出
    for new_path, old_path in filename_mapping.items():
        # パスからフォルダ名とファイル名を抽出
        old_dir, old_filename = os.path.split(old_path)
        new_dir, new_filename = os.path.split(new_path)
        
        # フォルダ名を取得（WindowsやJapaneseを含む階層構造は維持）
        folder_name = old_dir
        
        # フォルダマッピングにフォルダがなければ初期化
        if folder_name not in folder_mapping:
            folder_mapping[folder_name] = {}
        
        # 変更前ファイル名と変更後ファイル名をマッピング
        folder_mapping[folder_name][old_filename] = new_filename
    
    with open(os.path.join(BASE_DIR, "filename_mapping.json"), 'w', encoding='utf-8') as f:
        json.dump(folder_mapping, f, indent=2, ensure_ascii=False)

def rename_files(filename_mapping):
    """ファイルを実際に名前変更する"""
    for new_path, old_path in filename_mapping.items():
        # 絶対パスに変換
        old_abs_path = os.path.join(BASE_DIR, old_path)
        new_abs_path = os.path.join(BASE_DIR, new_path)
        
        # ファイルを名前変更
        if os.path.exists(old_abs_path):
            print(f"Renaming: {old_abs_path} -> {new_abs_path}")
            os.rename(old_abs_path, new_abs_path)
        else:
            print(f"File not found: {old_abs_path}")

def main():
    # 1. まずWindows以外のexamplesのファイルを処理
    non_windows_mapping, uuid_to_new_name = generate_non_windows_filenames()
    
    # 2. 次にWindows配下のexamplesのファイルを処理
    windows_mapping = generate_windows_filenames(uuid_to_new_name)
    
    # 3. 最後にexamples_japaneseのファイルを処理
    japanese_mapping = generate_japanese_filenames(uuid_to_new_name)
    
    # 全てのマッピングを結合
    combined_mapping = {**non_windows_mapping, **windows_mapping, **japanese_mapping}
    
    # マッピングをJSONに保存
    save_mapping_to_json(combined_mapping)
    
    # 実際にファイル名を変更するかどうか確認
    print(f"Found {len(combined_mapping)} files to rename.")
    print(f"- Non-Windows Examples: {len(non_windows_mapping)} files")
    print(f"- Windows Examples: {len(windows_mapping)} files")
    print(f"- Japanese Examples: {len(japanese_mapping)} files")
    confirmation = input("Proceed with renaming? (y/n): ")
    
    if confirmation.lower() == 'y':
        rename_files(combined_mapping)
        print("Files have been renamed successfully.")
    else:
        print("Renaming operation cancelled. Mapping saved to filename_mapping.json")

if __name__ == "__main__":
    main()
