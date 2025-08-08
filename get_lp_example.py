#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LP記事のサンプルを取得して構造を分析
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 親ディレクトリの.envを読み込み
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(parent_dir, '.env')
load_dotenv(dotenv_path)

def get_article(article_id):
    """記事を取得"""
    api_token = os.getenv('DOCBASE_ACCESS_TOKEN') or os.getenv('DOCBASE_API_TOKEN')
    team = os.getenv('DOCBASE_TEAM', 'go')
    
    if not api_token:
        print("❌ APIトークンが設定されていません")
        return None
    
    headers = {
        'X-DocBaseToken': api_token,
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.docbase.io/teams/{team}/posts/{article_id}"
    
    print(f"📖 記事ID {article_id} を取得中...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        article = response.json()
        
        # 記事内容を保存
        with open(f'lp_example_{article_id}.json', 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        
        # マークダウン本文を別ファイルに保存
        with open(f'lp_example_{article_id}.md', 'w', encoding='utf-8') as f:
            f.write(article['body'])
        
        print(f"✅ 記事を取得しました")
        print(f"📄 タイトル: {article['title']}")
        print(f"🔗 URL: {article['url']}")
        print(f"📝 タグ: {', '.join(article['tags'])}")
        print(f"\n💾 保存先:")
        print(f"   - lp_example_{article_id}.json")
        print(f"   - lp_example_{article_id}.md")
        
        return article
    else:
        print(f"❌ 記事の取得に失敗しました: {response.status_code}")
        return None

if __name__ == "__main__":
    # LP記事のサンプルを取得
    article_id = 3852378
    get_article(article_id)