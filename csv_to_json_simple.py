#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV/ExcelファイルからJSON形式に変換するスクリプト（pandas不要版）
"""

import csv
import json
import sys
import os
from typing import Dict, List

def parse_csv_to_json(csv_path: str) -> Dict:
    """CSVファイルをJSON形式に変換"""
    
    product_data = {}
    sku_list = []
    lp_structure = []
    page_details = []
    
    # CSVを読み込み
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # セクションごとに処理
    current_section = "basic"
    page_data = {}
    
    for row in rows:
        if not row or not row[0]:  # 空行
            continue
            
        # セクション判定
        if "====" in str(row[0]):
            if "SKU" in row[0]:
                current_section = "sku"
                continue
            elif "LP構成" in row[0]:
                current_section = "structure"
                continue
            elif "各ページ詳細" in row[0]:
                current_section = "page_details"
                continue
            elif "その他" in row[0]:
                current_section = "other"
                continue
        
        # 基本情報
        if current_section == "basic":
            if row[0] and row[0] != "項目名":
                product_data[row[0]] = row[1] if len(row) > 1 else ""
        
        # SKU情報
        elif current_section == "sku":
            if row[0] and row[0] != "sku_type":
                if len(row) >= 3:
                    sku_list.append({
                        'type': row[0],
                        'sku': row[1],
                        'jan': row[2]
                    })
        
        # LP構成
        elif current_section == "structure":
            if row[0] and row[0].startswith("page_"):
                lp_structure.append(row[1] if len(row) > 1 else "")
        
        # ページ詳細
        elif current_section == "page_details":
            if row[0] and row[0].startswith("page_"):
                key = row[0]
                value = row[1] if len(row) > 1 else ""
                
                # ページ番号を取得
                parts = key.split("_")
                if len(parts) >= 2:
                    try:
                        page_num = int(parts[1])
                        
                        # ページデータを初期化
                        if page_num not in page_data:
                            page_data[page_num] = {}
                        
                        # データタイプを判定
                        if "_text" in key:
                            page_data[page_num]['text'] = value.replace('\\n', '\n')
                        elif "_layout_note" in key:
                            page_data[page_num]['layout_note'] = value
                        elif "_image_" in key:
                            if 'images' not in page_data[page_num]:
                                page_data[page_num]['images'] = []
                            if value:  # 画像URLがある場合のみ追加
                                page_data[page_num]['images'].append(value)
                    except ValueError:
                        pass
        
        # その他の情報
        elif current_section == "other":
            if row[0] and len(row) > 1:
                product_data[row[0]] = row[1].replace('\\n', '\n')
    
    # ページ詳細を配列に変換
    for page_num in sorted(page_data.keys()):
        page_info = page_data[page_num]
        if not page_info.get('images'):
            page_info['has_images'] = True  # 画像準備中フラグ
        page_details.append(page_info)
    
    # 最終的なデータ構造を作成
    if sku_list:
        product_data['sku_list'] = sku_list
    if lp_structure:
        product_data['lp_structure'] = lp_structure
    if page_details:
        product_data['page_details'] = page_details
    
    return product_data

def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python csv_to_json_simple.py <CSVファイル>")
        print("\n例:")
        print("  python csv_to_json_simple.py templates/product_template.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"❌ ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    try:
        print(f"\n📊 CSV変換中: {input_file}")
        product_data = parse_csv_to_json(input_file)
        
        # JSONファイルを出力
        output_file = input_file.rsplit('.', 1)[0] + '_converted.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON変換完了: {output_file}")
        print(f"  商品名: {product_data.get('product_name', '未設定')}")
        print(f"  SKU数: {len(product_data.get('sku_list', []))}")
        print(f"  ページ数: {len(product_data.get('lp_structure', []))}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()