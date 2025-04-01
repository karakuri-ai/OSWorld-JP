import json
import os
import copy
import re

# ファイルパスを取得
base_dir = os.path.dirname(os.path.abspath(__file__))
mapping_file = os.path.join(base_dir, "filename_mapping.json")
test_all_file = os.path.join(base_dir, "test_all.json")
test_meta_file = os.path.join(base_dir, "test_meta.json")
test_small_jp_file = os.path.join(base_dir, "test_small_jp.json")
test_small_file = os.path.join(base_dir, "test_small.json")
test_all_jp_file = os.path.join(base_dir, "test_all_jp.json")

# filename_mapping.jsonを読み込む
with open(mapping_file, 'r') as f:
    filename_mapping = json.load(f)

# マッピング辞書を作成 (ファイルパス用とID用)
path_mapping = {}
# ディレクトリ情報を含むUUIDマッピング
dir_uuid_mapping = {}  # {dir_path: {uuid: new_id}}

# 逆引きマッピングも作成（デバッグと検証用）
reverse_id_mapping = {}

for category, files in filename_mapping.items():
    # カテゴリ別のマッピングを初期化
    if category not in dir_uuid_mapping:
        dir_uuid_mapping[category] = {}
        
    for old_name, new_name in files.items():
        # ファイルパスのマッピング
        old_path = f"{category}/{old_name}"
        new_path = f"{category}/{new_name}"
        path_mapping[old_path] = new_path
        
        # UUIDを抽出（拡張子なしのファイル名部分）
        uuid = old_name.replace(".json", "")
        new_id = new_name.replace(".json", "")
        
        # カテゴリ別UUIDマッピングを追加
        dir_uuid_mapping[category][uuid] = new_id
        
        # 逆引きマッピングを更新
        if new_id not in reverse_id_mapping:
            reverse_id_mapping[new_id] = {}
        reverse_id_mapping[new_id][category] = uuid
        
        # 日本語版のマッピングも追加
        if not category.startswith("examples_japanese"):
            j_category = f"examples_japanese/{category.replace('examples/', '')}"
            
            # 日本語版カテゴリのマッピングを初期化
            if j_category not in dir_uuid_mapping:
                dir_uuid_mapping[j_category] = {}
            
            j_old_path = f"{j_category}/J_{old_name}"
            j_new_path = f"{j_category}/J_{new_name}"
            path_mapping[j_old_path] = j_new_path
            
            # 日本語版IDのマッピング
            j_uuid = f"J_{uuid}"
            j_new_id = f"J_{new_id}"
            dir_uuid_mapping[j_category][uuid] = new_id  # 元のUUIDも変換できるように
            dir_uuid_mapping[j_category][j_uuid] = j_new_id  # J_プレフィックス付きも変換できるように
            
            # 逆引きマッピングを更新
            if j_new_id not in reverse_id_mapping:
                reverse_id_mapping[j_new_id] = {}
            reverse_id_mapping[j_new_id][j_category] = j_uuid

# UUIDを検出する関数
def could_be_uuid(s):
    # 標準的なUUID形式をチェック
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    # UUIDとして登録済みか、パターンにマッチするかをチェック
    for category_mapping in dir_uuid_mapping.values():
        if str(s) in category_mapping:
            return True
    
    return bool(uuid_pattern.match(str(s).lower()))

# 変換状況を追跡するカウンター
conversion_stats = {
    'converted_keys': 0,
    'converted_values': 0,
    'skipped_items': 0
}

# ディレクトリ情報とUUIDを組み合わせて検索するための関数
def convert_uuid_with_dir_context(uuid_str, category_context=None, use_j_prefix=False):
    # J_プレフィックスの処理
    original_uuid = uuid_str
    if use_j_prefix and not uuid_str.startswith("J_"):
        uuid_with_j = f"J_{uuid_str}"
    else:
        uuid_with_j = uuid_str
    
    # 1. 指定されたカテゴリで検索
    if category_context and category_context in dir_uuid_mapping:
        category_mapping = dir_uuid_mapping[category_context]
        
        # カテゴリ内で元のUUIDを検索
        if uuid_str in category_mapping:
            result = category_mapping[uuid_str]
            if use_j_prefix and not result.startswith("J_") and not uuid_str.startswith("J_"):
                return f"J_{result}"
            return result
            
        # カテゴリ内でJ_付きUUIDを検索
        if uuid_with_j in category_mapping:
            return category_mapping[uuid_with_j]
    
    # 2. すべてのカテゴリを検索（カテゴリ指定がない場合や、指定カテゴリで見つからない場合）
    for cat, mapping in dir_uuid_mapping.items():
        # 日本語版のカテゴリを優先（use_j_prefixがTrueの場合）
        if use_j_prefix and not cat.startswith("examples_japanese"):
            continue
            
        if uuid_str in mapping:
            result = mapping[uuid_str]
            if use_j_prefix and not result.startswith("J_") and not uuid_str.startswith("J_"):
                return f"J_{result}"
            return result
            
        if uuid_with_j in mapping:
            return mapping[uuid_with_j]
    
    # 3. 変換できない場合は元の値を返す（J_プレフィックスの処理を適用）
    if use_j_prefix and not original_uuid.startswith("J_"):
        return f"J_{original_uuid}"
    return original_uuid

# JSONオブジェクト内のUUIDをすべて変換する再帰関数
def convert_uuids_in_json(obj, category_context=None, use_j_prefix=False, path="root"):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            # キーがUUIDの場合、変換する
            orig_key = key
            new_key = key
            
            if could_be_uuid(key):
                new_key = convert_uuid_with_dir_context(key, category_context, use_j_prefix)
                if new_key != key:
                    conversion_stats['converted_keys'] += 1
            
            # 値を再帰的に処理（現在のパスを更新）
            new_dict[new_key] = convert_uuids_in_json(
                value, 
                category_context,
                use_j_prefix, 
                f"{path}.{orig_key}"
            )
        return new_dict
    elif isinstance(obj, list):
        # リストの場合は各要素を再帰的に処理
        return [convert_uuids_in_json(item, category_context, use_j_prefix, f"{path}[{i}]") for i, item in enumerate(obj)]
    elif isinstance(obj, str) and could_be_uuid(obj):
        # 文字列がUUIDの場合、変換する
        new_id = convert_uuid_with_dir_context(obj, category_context, use_j_prefix)
        if new_id != obj:
            conversion_stats['converted_values'] += 1
            return new_id
        else:
            conversion_stats['skipped_items'] += 1
    
    # その他の型や変換対象でないものはそのまま返す
    return obj

# ファイルを読み込み、パスとIDを変換する関数
def convert_file_paths_and_ids(file_path, is_japanese=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"警告: ファイル {file_path} が見つかりません。スキップします。")
        return {}
    except json.JSONDecodeError:
        print(f"警告: ファイル {file_path} の解析に失敗しました。JSONフォーマットを確認してください。")
        return {}
    
    # 変換統計をリセット
    global conversion_stats
    conversion_stats = {
        'converted_keys': 0,
        'converted_values': 0,
        'skipped_items': 0
    }
    
    new_data = {}
    for path, content in data.items():
        # パスを変換
        new_path = path_mapping.get(path, path)
        if new_path != path:
            print(f"パス変換: {path} -> {new_path}")
        
        # カテゴリ情報を抽出（ディレクトリパス）
        path_parts = path.split('/')
        if len(path_parts) >= 2:
            category_dir = '/'.join(path_parts[:-1])
        else:
            category_dir = None
        
        # 内容のUUIDを変換（カテゴリ情報を渡す）
        new_content = convert_uuids_in_json(content, category_dir, is_japanese)
        new_data[new_path] = new_content
    
    print(f"ファイル {os.path.basename(file_path)} の変換結果:")
    print(f"  - キー変換数: {conversion_stats['converted_keys']}")
    print(f"  - 値変換数: {conversion_stats['converted_values']}")
    print(f"  - スキップされた項目: {conversion_stats['skipped_items']}")
    
    return new_data

# 各ファイルを変換して保存
files_to_convert = [
    (test_all_file, "converted_test_all.json", False),
    (test_meta_file, "converted_test_meta.json", False),
    (test_small_jp_file, "converted_test_small_jp.json", True),
    (test_small_file, "converted_test_small.json", False),
    (test_all_jp_file, "converted_test_all_jp.json", True)
]

print(f"変換を開始します。マッピング数: {len(dir_uuid_mapping)} 個のカテゴリ")

for src_file, dest_file, is_japanese in files_to_convert:
    print(f"\n{os.path.basename(src_file)} の処理を開始...")
    converted_data = convert_file_paths_and_ids(src_file, is_japanese)
    
    # 処理結果がある場合のみ保存
    if converted_data:
        with open(os.path.join(base_dir, dest_file), 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, indent=2, ensure_ascii=False)
        print(f"保存完了: {dest_file}")

print("\n変換が完了しました！")
print("作成されたファイル:")
for _, dest_file, _ in files_to_convert:
    if os.path.exists(os.path.join(base_dir, dest_file)):
        print(f"- {dest_file}")
