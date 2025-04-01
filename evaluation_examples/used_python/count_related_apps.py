#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from collections import Counter
import sys
import csv

def count_related_apps():
    """
    evaluation_examples ディレクトリ内のJSONファイルを探し、
    related_apps フィールド内のアプリケーションの出現回数をカウントする
    """
    # ベースディレクトリ設定
    base_dir = "/Users/shojibumbu/dev/osworld/evaluation_examples/examples/multiapps"
    
    # 分析結果
    app_counter = Counter()
    file_app_mapping = {}
    total_files = 0
    
    # ディレクトリを走査してJSONファイルを検索
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # related_appsフィールドがあるか確認
                        if "related_apps" in data and isinstance(data["related_apps"], list):
                            total_files += 1
                            file_name = os.path.basename(file_path)
                            
                            # ファイルごとのアプリリストを記録
                            app_list = data["related_apps"]
                            file_app_mapping[file_name] = app_list
                            
                            # 各アプリをカウント
                            for app in app_list:
                                app_counter[app] += 1
                                
                except Exception as e:
                    print(f"{file_path}の読み込み中にエラーが発生しました: {e}", file=sys.stderr)
    
    # ファイルごとのアプリリストをCSVに保存
    file_apps_csv_path = os.path.join(base_dir, "file_apps_mapping.csv")
    with open(file_apps_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['file_name', 'apps'])
        for file_name, apps in file_app_mapping.items():
            writer.writerow([file_name, ', '.join(apps)])
    
    # 詳細結果をJSONファイルに保存
    json_path = os.path.join(base_dir, "related_apps_detail.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total_files": total_files,
            "app_counts": dict(app_counter),
            "file_app_mapping": file_app_mapping
        }, f, indent=2, ensure_ascii=False)
    
    return app_counter, total_files, file_app_mapping

def main():
    # 実行
    app_counter, total_files, file_app_mapping = count_related_apps()
    
    # 結果を表示
    print(f"'related_apps'フィールドを持つファイル数: {total_files}")
    print(f"見つかったユニークなアプリ数: {len(app_counter)}")
    
    print("\nアプリケーションの出現回数:")
    for app, count in app_counter.most_common():
        percentage = (count / total_files) * 100 if total_files > 0 else 0
        print(f"{app}: {count} ({percentage:.2f}%)")
    
    base_dir = "/Users/shojibumbu/dev/osworld/evaluation_examples/examples/multiapps"
    print("\n結果は以下のファイルに保存されました:")
    print(f"  - ファイルごとのアプリリストCSV: {os.path.join(base_dir, 'file_apps_mapping.csv')}")
    print(f"  - JSON形式の詳細結果: {os.path.join(base_dir, 'related_apps_detail.json')}")

if __name__ == "__main__":
    main()
