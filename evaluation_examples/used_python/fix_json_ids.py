#!/usr/bin/env python3
import os
import json
import glob
from pathlib import Path

def fix_json_ids():
    # 処理対象のルートディレクトリを設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 英語例と日本語例のディレクトリパスを設定
    examples_dir = os.path.join(base_dir, "examples")
    japanese_dir = os.path.join(base_dir, "examples_japanese")
    
    # 統計情報の初期化
    stats = {
        "total_files": 0,
        "updated_files": 0,
        "skipped_files": 0,
        "error_files": 0
    }
    
    # 英語と日本語の例を処理
    for root_dir in [examples_dir, japanese_dir]:
        if not os.path.exists(root_dir):
            print(f"ディレクトリが見つかりません: {root_dir}")
            continue
        
        # 再帰的にすべてのJSONファイルを取得
        json_files = glob.glob(os.path.join(root_dir, "**/*.json"), recursive=True)
        stats["total_files"] += len(json_files)
        
        for json_file in json_files:
            try:
                # ファイル名（拡張子なし）を取得
                filename_without_ext = os.path.splitext(os.path.basename(json_file))[0]
                
                # JSONファイルを読み込む
                with open(json_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"JSONデコードエラー: {json_file}")
                        stats["error_files"] += 1
                        continue
                
                # "id"フィールドが存在し、ファイル名と異なる場合に更新
                if "id" in data and data["id"] != filename_without_ext:
                    print(f"更新: {json_file}")
                    print(f"  旧ID: {data['id']}")
                    print(f"  新ID: {filename_without_ext}")
                    
                    # IDを更新
                    data["id"] = filename_without_ext
                    
                    # 更新したJSONを書き戻す
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    stats["updated_files"] += 1
                else:
                    stats["skipped_files"] += 1
            
            except Exception as e:
                print(f"エラー ({json_file}): {str(e)}")
                stats["error_files"] += 1
    
    # 結果を表示
    print("\n===== 処理結果 =====")
    print(f"処理ファイル数: {stats['total_files']}")
    print(f"更新ファイル数: {stats['updated_files']}")
    print(f"スキップファイル数: {stats['skipped_files']}")
    print(f"エラーファイル数: {stats['error_files']}")

if __name__ == "__main__":
    fix_json_ids()
