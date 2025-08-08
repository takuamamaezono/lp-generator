#!/usr/bin/env python3
"""
LP欄自動生成システム
商品情報を入力するとDocbase用のLP欄のマークダウンを生成します
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import sys


class LPGenerator:
    """LP欄生成クラス"""
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        # ディレクトリ作成
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_lp(self, product_info: Dict) -> str:
        """商品情報からLP欄のマークダウンを生成"""
        
        # 必須項目チェック
        required_fields = ['product_name', 'catch_copy', 'price', 'features']
        for field in required_fields:
            if field not in product_info:
                raise ValueError(f"必須項目 '{field}' が入力されていません")
        
        # LP欄の生成
        lp_content = f"""# {product_info['product_name']} LP欄

## 🎯 キャッチコピー
> **{product_info['catch_copy']}**

---

## 📦 商品概要

### 商品名
{product_info['product_name']}

### 価格
**{product_info['price']}円**{' (税込)' if product_info.get('tax_included', True) else ' (税抜)'}

### カテゴリ
{product_info.get('category', '未分類')}

---

## ✨ 主な特徴

"""
        # 特徴リスト
        for i, feature in enumerate(product_info['features'], 1):
            lp_content += f"### {i}. {feature['title']}\n"
            lp_content += f"{feature['description']}\n\n"
        
        # ターゲット顧客
        if 'target_customer' in product_info:
            lp_content += f"""## 👥 こんな方におすすめ

{product_info['target_customer']}

"""
        
        # 解決する問題
        if 'solve_problems' in product_info:
            lp_content += f"""## 💡 解決できる課題

"""
            for problem in product_info['solve_problems']:
                lp_content += f"- {problem}\n"
            lp_content += "\n"
        
        # 画像セクション
        if 'main_image' in product_info or 'sub_images' in product_info:
            lp_content += "## 🖼️ 商品画像\n\n"
            
            if 'main_image' in product_info:
                lp_content += f"### メイン画像\n![{product_info['product_name']}]({product_info['main_image']})\n\n"
            
            if 'sub_images' in product_info:
                lp_content += "### 詳細画像\n"
                for i, img in enumerate(product_info['sub_images'], 1):
                    lp_content += f"![詳細画像{i}]({img})\n"
                lp_content += "\n"
        
        # 使用シーン
        if 'use_scenes' in product_info:
            lp_content += "## 🎬 使用シーン\n\n"
            for scene in product_info['use_scenes']:
                lp_content += f"- {scene}\n"
            lp_content += "\n"
        
        # CTA（行動喚起）
        lp_content += "## 🛒 ご購入・お問い合わせ\n\n"
        
        if 'purchase_link' in product_info:
            lp_content += f"### [今すぐ購入する]({product_info['purchase_link']})\n\n"
        
        if 'contact_info' in product_info:
            lp_content += f"### お問い合わせ先\n{product_info['contact_info']}\n\n"
        
        # 補足情報
        if 'notes' in product_info:
            lp_content += f"## 📝 補足情報\n\n{product_info['notes']}\n\n"
        
        # フッター
        lp_content += f"\n---\n\n*最終更新: {datetime.now().strftime('%Y年%m月%d日')}*\n"
        
        return lp_content
    
    def save_template(self, template_name: str, product_info: Dict):
        """テンプレートとして保存"""
        template_path = os.path.join(self.template_dir, f"{template_name}.json")
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(product_info, f, ensure_ascii=False, indent=2)
        print(f"テンプレート '{template_name}' を保存しました: {template_path}")
    
    def load_template(self, template_name: str) -> Dict:
        """テンプレートを読み込み"""
        template_path = os.path.join(self.template_dir, f"{template_name}.json")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"テンプレート '{template_name}' が見つかりません")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_templates(self) -> List[str]:
        """利用可能なテンプレート一覧"""
        templates = []
        for file in os.listdir(self.template_dir):
            if file.endswith('.json'):
                templates.append(file.replace('.json', ''))
        return templates
    
    def save_output(self, content: str, filename: str):
        """生成したLPを保存"""
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"LP欄を保存しました: {output_path}")
        return output_path


def interactive_input():
    """対話式で商品情報を入力"""
    print("=== LP欄生成システム ===")
    print("商品情報を入力してください（Ctrl+Cで中断）\n")
    
    product_info = {}
    
    try:
        # 基本情報
        product_info['product_name'] = input("商品名: ").strip()
        product_info['catch_copy'] = input("キャッチコピー: ").strip()
        product_info['price'] = input("価格（数字のみ）: ").strip()
        product_info['tax_included'] = input("税込み？ (y/n) [y]: ").strip().lower() != 'n'
        product_info['category'] = input("カテゴリ（省略可）: ").strip()
        
        # 特徴
        print("\n主な特徴を入力してください（3〜5個推奨）")
        features = []
        i = 1
        while True:
            print(f"\n特徴{i}:")
            title = input("  タイトル（空欄で終了）: ").strip()
            if not title:
                break
            description = input("  説明: ").strip()
            features.append({'title': title, 'description': description})
            i += 1
        product_info['features'] = features
        
        # ターゲット顧客
        target = input("\nターゲット顧客（省略可）: ").strip()
        if target:
            product_info['target_customer'] = target
        
        # 解決する問題
        print("\n解決できる課題（空欄で終了）:")
        problems = []
        while True:
            problem = input("- ").strip()
            if not problem:
                break
            problems.append(problem)
        if problems:
            product_info['solve_problems'] = problems
        
        # 画像
        main_img = input("\nメイン画像URL（省略可）: ").strip()
        if main_img:
            product_info['main_image'] = main_img
        
        # CTA
        purchase = input("\n購入リンクURL（省略可）: ").strip()
        if purchase:
            product_info['purchase_link'] = purchase
        
        contact = input("お問い合わせ先（省略可）: ").strip()
        if contact:
            product_info['contact_info'] = contact
        
        return product_info
        
    except KeyboardInterrupt:
        print("\n\n入力を中断しました")
        sys.exit(0)


def main():
    """メイン処理"""
    generator = LPGenerator()
    
    print("LP欄生成システムへようこそ！\n")
    print("1. 新規作成")
    print("2. テンプレートから作成")
    print("3. サンプルデータで実行")
    
    choice = input("\n選択してください (1-3): ").strip()
    
    if choice == '1':
        # 新規作成
        product_info = interactive_input()
        
    elif choice == '2':
        # テンプレートから
        templates = generator.list_templates()
        if not templates:
            print("テンプレートがありません。新規作成してください。")
            product_info = interactive_input()
        else:
            print("\n利用可能なテンプレート:")
            for i, t in enumerate(templates, 1):
                print(f"{i}. {t}")
            
            idx = int(input("\n番号を選択: ")) - 1
            product_info = generator.load_template(templates[idx])
            print(f"\nテンプレート '{templates[idx]}' を読み込みました")
            
            # 編集するか確認
            if input("このまま使用しますか？ (y/n) [y]: ").strip().lower() == 'n':
                # TODO: 編集機能
                print("編集機能は準備中です")
    
    elif choice == '3':
        # サンプルデータ
        product_info = {
            "product_name": "PowerArQ Pro",
            "catch_copy": "どこでも電源、いつでも安心。大容量ポータブル電源",
            "price": "132000",
            "tax_included": True,
            "category": "ポータブル電源",
            "features": [
                {
                    "title": "大容量1002.4Wh",
                    "description": "家電製品を長時間使用できる大容量バッテリー。停電時も安心です。"
                },
                {
                    "title": "高出力1000W",
                    "description": "ドライヤーや電子レンジなど、消費電力の大きい家電も使用可能。"
                },
                {
                    "title": "充電方法が豊富",
                    "description": "AC充電、ソーラー充電、シガーソケット充電に対応。"
                }
            ],
            "target_customer": "キャンプや車中泊を楽しむ方、災害対策をしたい方、屋外作業をされる方",
            "solve_problems": [
                "キャンプ場で電源が使えない",
                "停電時の備えがない",
                "屋外イベントで電源確保が難しい"
            ],
            "main_image": "https://example.com/powerarq-pro-main.jpg",
            "purchase_link": "https://example.com/shop/powerarq-pro",
            "contact_info": "お電話: 0120-xxx-xxx\nメール: support@example.com"
        }
    
    else:
        print("無効な選択です")
        return
    
    # LP生成
    lp_content = generator.generate_lp(product_info)
    
    # プレビュー
    print("\n=== 生成されたLP欄 ===\n")
    print(lp_content)
    
    # 保存
    if input("\n保存しますか？ (y/n) [y]: ").strip().lower() != 'n':
        filename = f"lp_{product_info['product_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        generator.save_output(lp_content, filename)
        
        # テンプレートとして保存
        if input("テンプレートとして保存しますか？ (y/n) [n]: ").strip().lower() == 'y':
            template_name = input("テンプレート名: ").strip()
            generator.save_template(template_name, product_info)


if __name__ == "__main__":
    main()