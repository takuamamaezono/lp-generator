#!/usr/bin/env python3
"""
Docbase LP欄アップローダー
生成したLP欄をDocbaseに直接投稿・更新するスクリプト
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional, Dict

# 親ディレクトリからdotenvを読み込む
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(parent_dir, '.env')
load_dotenv(dotenv_path)


class DocbaseLPUploader:
    """Docbase LP欄アップロードクラス"""
    
    def __init__(self):
        self.api_token = os.getenv('DOCBASE_ACCESS_TOKEN') or os.getenv('DOCBASE_API_TOKEN')
        self.team = os.getenv('DOCBASE_TEAM', 'go')
        
        if not self.api_token:
            raise ValueError("環境変数 DOCBASE_ACCESS_TOKEN または DOCBASE_API_TOKEN を設定してください")
        
        self.base_url = f"https://api.docbase.io/teams/{self.team}"
        self.headers = {
            'X-DocBaseToken': self.api_token,
            'Content-Type': 'application/json'
        }
    
    def create_lp_post(self, title: str, content: str, tags: list = None) -> Dict:
        """新規LP記事を作成"""
        
        if tags is None:
            tags = ['LP欄', '商品紹介', '自動生成']
        
        data = {
            'title': title,
            'body': content,
            'tags': tags,
            'scope': 'private',  # 従業員のみ（重要）
            'groups': [],
            'notice': False
        }
        
        response = requests.post(
            f"{self.base_url}/posts",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ LP記事を作成しました！")
            print(f"   タイトル: {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   ID: {result['id']}")
            return result
        else:
            print(f"❌ エラーが発生しました: {response.status_code}")
            print(response.text)
            raise Exception(f"Docbase API Error: {response.status_code}")
    
    def update_lp_post(self, post_id: int, title: str, content: str, tags: list = None) -> Dict:
        """既存のLP記事を更新"""
        
        if tags is None:
            tags = ['LP欄', '商品紹介', '自動生成', '更新済み']
        
        data = {
            'title': title,
            'body': content,
            'tags': tags,
            'scope': 'private'  # 従業員のみ（重要）
        }
        
        response = requests.patch(
            f"{self.base_url}/posts/{post_id}",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ LP記事を更新しました！")
            print(f"   タイトル: {result['title']}")
            print(f"   URL: {result['url']}")
            return result
        else:
            print(f"❌ エラーが発生しました: {response.status_code}")
            print(response.text)
            raise Exception(f"Docbase API Error: {response.status_code}")
    
    def search_lp_posts(self, product_name: str) -> list:
        """商品名でLP記事を検索"""
        
        params = {
            'q': f'title:{product_name} tag:LP欄',
            'per_page': 10
        }
        
        response = requests.get(
            f"{self.base_url}/posts",
            headers=self.headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()['posts']
        else:
            print(f"検索エラー: {response.status_code}")
            return []
    
    def create_or_update_lp(self, product_name: str, lp_content: str):
        """LP記事を作成または更新"""
        
        # 既存記事を検索
        existing_posts = self.search_lp_posts(product_name)
        
        title = f"{product_name} - LP欄"
        
        if existing_posts:
            # 既存記事があれば更新
            post = existing_posts[0]
            print(f"\n既存のLP記事が見つかりました: {post['title']}")
            
            if input("更新しますか？ (y/n) [y]: ").strip().lower() != 'n':
                self.update_lp_post(post['id'], title, lp_content)
            else:
                print("更新をキャンセルしました")
        else:
            # 新規作成
            print(f"\n新規LP記事を作成します: {title}")
            
            if input("作成しますか？ (y/n) [y]: ").strip().lower() != 'n':
                self.create_lp_post(title, lp_content)
            else:
                print("作成をキャンセルしました")


def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("使い方: python docbase_lp_uploader.py <LP欄マークダウンファイル>")
        print("例: python docbase_lp_uploader.py output/lp_PowerArQ_Pro_20240124_150000.md")
        sys.exit(1)
    
    lp_file = sys.argv[1]
    
    if not os.path.exists(lp_file):
        print(f"ファイルが見つかりません: {lp_file}")
        sys.exit(1)
    
    # LP内容を読み込み
    with open(lp_file, 'r', encoding='utf-8') as f:
        lp_content = f.read()
    
    # タイトルから商品名を抽出
    lines = lp_content.split('\n')
    product_name = None
    for line in lines:
        if line.startswith('# ') and 'LP欄' in line:
            product_name = line.replace('# ', '').replace(' LP欄', '').strip()
            break
    
    if not product_name:
        product_name = input("商品名を入力してください: ").strip()
    
    # アップロード実行
    try:
        uploader = DocbaseLPUploader()
        uploader.create_or_update_lp(product_name, lp_content)
        
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()