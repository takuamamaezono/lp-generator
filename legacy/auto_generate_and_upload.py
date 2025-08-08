#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSVから自動でLPラフ案を生成してDocbaseにアップロードする統合スクリプト
"""

import os
import sys
import json
import subprocess
from csv_to_json import parse_csv_to_json, parse_excel_to_json
from lp_rough_generator import LPRoughGenerator
from docbase_lp_uploader import DocbaseLPUploader

def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("\n📋 使用方法:")
        print("  python auto_generate_and_upload.py <CSVまたはExcelファイル> [オプション]")
        print("\nオプション:")
        print("  --upload    : Docbaseに自動アップロード")
        print("  --dry-run   : 生成のみ（アップロードしない）")
        print("\n例:")
        print("  python auto_generate_and_upload.py templates/product_template.csv --upload")
        print("  python auto_generate_and_upload.py data/商品情報.xlsx --dry-run")
        sys.exit(1)
    
    input_file = sys.argv[1]
    upload_flag = "--upload" in sys.argv
    dry_run = "--dry-run" in sys.argv
    
    if not os.path.exists(input_file):
        print(f"❌ ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    try:
        print("\n🚀 LPラフ案自動生成を開始します...")
        print("=" * 50)
        
        # Step 1: CSV/ExcelをJSONに変換
        print("\n📊 Step 1: データ変換中...")
        if input_file.endswith('.csv'):
            product_data = parse_csv_to_json(input_file)
        elif input_file.endswith(('.xlsx', '.xls')):
            product_data = parse_excel_to_json(input_file)
        else:
            print("❌ サポートされていないファイル形式です")
            sys.exit(1)
        
        print(f"  ✅ 商品名: {product_data.get('product_name', '未設定')}")
        print(f"  ✅ SKU数: {len(product_data.get('sku_list', []))}")
        print(f"  ✅ ページ数: {len(product_data.get('lp_structure', []))}")
        
        # Step 2: LPラフ案を生成
        print("\n📝 Step 2: LPラフ案生成中...")
        generator = LPRoughGenerator()
        lp_content = generator.generate_lp_rough(product_data)
        
        # ファイルに保存
        filepath = generator.save_lp_rough(lp_content, product_data['product_name'])
        print(f"  ✅ 生成完了: {filepath}")
        
        # プレビュー表示
        print("\n📄 プレビュー（最初の500文字）:")
        print("-" * 40)
        print(lp_content[:500])
        print("-" * 40)
        
        # Step 3: Docbaseにアップロード（オプション）
        if upload_flag and not dry_run:
            print("\n📤 Step 3: Docbaseにアップロード中...")
            
            uploader = DocbaseLPUploader()
            
            # タイトルを作成
            title = f"{product_data['product_name']} LPラフ案"
            
            # タグを設定
            tags = ['LPラフ案', '自動生成', product_data['product_name']]
            
            # 既存記事を検索
            existing_posts = uploader.search_lp_posts(product_data['product_name'])
            
            if existing_posts:
                # 既存記事を更新
                post_id = existing_posts[0]['id']
                result = uploader.update_lp_post(post_id, title, lp_content, tags)
                print(f"  ✅ 記事を更新しました")
            else:
                # 新規作成
                result = uploader.create_lp_post(title, lp_content, tags)
                print(f"  ✅ 新規記事を作成しました")
            
            print(f"  📎 URL: {result['url']}")
            print(f"  🆔 ID: {result['id']}")
            
        elif dry_run:
            print("\n⚠️ ドライランモード: Docbaseへのアップロードはスキップしました")
        else:
            print("\n💡 Docbaseにアップロードするには --upload オプションを追加してください")
        
        # 完了メッセージ
        print("\n" + "=" * 50)
        print("✨ すべての処理が完了しました！")
        
        if not upload_flag:
            print("\n次のステップ:")
            print(f"1. 生成されたファイルを確認: {filepath}")
            print("2. Docbaseにアップロード:")
            print(f"   python docbase_lp_uploader.py {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()