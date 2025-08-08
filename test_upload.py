#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テスト用のDocbaseアップロードスクリプト
"""

import os
from docbase_lp_uploader import DocbaseLPUploader

def main():
    """メイン処理"""
    
    # アップロード対象のファイル
    lp_file = "output/lp_rough_商品名をここに入力_20250808_071110.md"
    
    if not os.path.exists(lp_file):
        print(f"❌ ファイルが見つかりません: {lp_file}")
        return
    
    # ファイル内容を読み込み
    with open(lp_file, 'r', encoding='utf-8') as f:
        lp_content = f.read()
    
    try:
        # Docbaseアップローダーを初期化
        uploader = DocbaseLPUploader()
        
        # テスト用の記事情報
        title = "【テスト】LPラフ案自動生成テスト"
        tags = ['LPラフ案', '自動生成', 'テスト']
        
        print(f"📤 Docbaseにアップロード中...")
        print(f"タイトル: {title}")
        
        # 既存のテスト記事があるか検索
        existing_posts = uploader.search_lp_posts("テスト")
        
        if existing_posts:
            # 既存記事を更新
            post_id = existing_posts[0]['id']
            result = uploader.update_lp_post(post_id, title, lp_content, tags)
            print(f"✅ 既存記事を更新しました")
        else:
            # 新規作成
            result = uploader.create_lp_post(title, lp_content, tags)
            print(f"✅ 新規記事を作成しました")
        
        print(f"📎 URL: {result['url']}")
        print(f"🆔 ID: {result['id']}")
        print(f"\n🎉 Docbaseアップロード完了！")
        
    except Exception as e:
        print(f"❌ アップロードエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()