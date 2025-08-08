#!/usr/bin/env python3
"""
初心者向けマニュアルをDocbaseに投稿するスクリプト
"""

import os
import requests
import json
from datetime import datetime

# 環境変数から設定を取得
DOCBASE_ACCESS_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
DOCBASE_TEAM = os.getenv('DOCBASE_TEAM', 'go')

if not DOCBASE_ACCESS_TOKEN:
    print("❌ DOCBASE_ACCESS_TOKEN が設定されていません")
    print("📝 .envファイルでトークンを設定してください")
    exit(1)

def read_manual_file():
    """マニュアルファイルを読み込み"""
    manual_file = "DOCBASE_BEGINNER_MANUAL.md"
    
    if not os.path.exists(manual_file):
        print(f"❌ マニュアルファイルが見つかりません: {manual_file}")
        exit(1)
    
    with open(manual_file, 'r', encoding='utf-8') as f:
        return f.read()

def upload_to_docbase(title, body, tags=None):
    """DocbaseにMarkdownを投稿"""
    url = f"https://{DOCBASE_TEAM}.docbase.io/api/v1/posts"
    
    headers = {
        'X-DocBaseToken': DOCBASE_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': title,
        'body': body,
        'draft': False,
        'scope': 'everyone',
        'notice': True
    }
    
    if tags:
        data['tags'] = tags
    
    try:
        print("📤 Docbaseに投稿中...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 201:
            result = response.json()
            post_url = result.get('url', '')
            print(f"✅ 投稿完了！")
            print(f"🔗 URL: {post_url}")
            return post_url
        else:
            print(f"❌ 投稿エラー: {response.status_code}")
            print(f"📄 レスポンス: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 投稿中にエラーが発生: {e}")
        return None

def main():
    print("🚀 LPラフ案自動生成システム - 初心者向けマニュアル投稿")
    print("=" * 60)
    
    # マニュアルファイル読み込み
    manual_content = read_manual_file()
    
    # 投稿タイトル
    title = "🚀 LPラフ案自動生成システム - 超初心者向けマニュアル（GitHub対応版）"
    
    # タグ設定
    tags = [
        "LP生成システム",
        "自動化ツール",
        "GitHub",
        "Docker",
        "競合分析",
        "初心者向け",
        "マニュアル"
    ]
    
    # Docbaseに投稿
    post_url = upload_to_docbase(title, manual_content, tags)
    
    if post_url:
        print("\n🎉 マニュアル投稿が完了しました！")
        print(f"📖 チームメンバーは以下のURLでマニュアルを確認できます：")
        print(f"🔗 {post_url}")
        print("\n💡 このマニュアルを使って、誰でも簡単にLP生成システムを利用できます！")
    else:
        print("\n❌ 投稿に失敗しました。設定を確認してください。")

if __name__ == "__main__":
    main()