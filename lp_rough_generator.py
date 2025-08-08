#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LPラフ案自動生成システム
商品データを入力するとDocbase用のLPラフ案を自動生成します
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import sys

class LPRoughGenerator:
    """LPラフ案生成クラス"""
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        # ディレクトリ作成
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_lp_rough(self, product_data: Dict) -> str:
        """商品データからLPラフ案を生成"""
        
        # 必須項目チェック
        required_fields = ['product_name', 'purpose', 'target_platform']
        for field in required_fields:
            if field not in product_data:
                raise ValueError(f"必須項目 '{field}' が入力されていません")
        
        # LPラフ案の生成
        lp_content = f"""# LPラフ
## 作成の目的、意図
{product_data.get('purpose', '商品の販売促進のため')}

## 対象商品
### 商品名
{product_data['product_name']}

### SKU・JAN
"""
        
        # SKU/JANテーブル
        if 'sku_list' in product_data and product_data['sku_list']:
            lp_content += "| 種類 | SKU | JAN |\n| --- | --- | --- |\n"
            for item in product_data['sku_list']:
                lp_content += f"| {item.get('type', '')} | {item.get('sku', '')} | {item.get('jan', '')} |\n"
        else:
            lp_content += "| 種類 | SKU | JAN |\n| --- | --- | --- |\n| - | - | - |\n"
        
        lp_content += "\n"
        
        # 基本情報
        lp_content += """## 基本情報
### バナースペック
| 項目 | 内容 |
| --- | --- |
| サイズ | PC:W1200px、SP：850px、flick：1000px |
| 拡張子 | JPG |
| カラーモード | RGB |
| 画質 | なるべく画質優先で大丈夫です |
| 圧縮方式 | プログレッシブとベースラインで容量が小さい方、同じ容量の場合はプログレッシブ優先 |
| 解像度 | 72ppi |
| アンチエイリアス | 文字に最適 |
| ICCプロファイル | 消してください |


### フォント、カラー指定

"""
        
        if product_data.get('tonmana_url'):
            lp_content += f"下記、トンマナを踏まえて作成お願いします。\n{product_data['tonmana_url']}\n\n"
        else:
            lp_content += "トンマナに関しては別途共有します。\n\n"
        
        if product_data.get('base_data_url'):
            lp_content += f"### ベースのデータ\n\n{product_data['base_data_url']}\n\n"
        
        # LP構成
        lp_content += "---\n# LP構成\n| 枚数 | コンテンツ概要 |\n| --- | --- |\n"
        
        # デフォルトの構成またはカスタム構成
        if 'lp_structure' in product_data and product_data['lp_structure']:
            for i, content in enumerate(product_data['lp_structure'], 1):
                lp_content += f"| {i}枚目 | {content} |\n"
        else:
            # デフォルト構成
            default_structure = [
                "TOPキャッチ",
                "売れている訴求・実績",
                "ブランド価値・安全性",
                "メイン機能・特徴1",
                "メイン機能・特徴2",
                "使用シーン",
                "サイズ・スペック詳細",
                "付属品・同梱物",
                "保証・アフターサービス",
                "よくある質問"
            ]
            for i, content in enumerate(default_structure, 1):
                lp_content += f"| {i}枚目 | {content} |\n"
        
        lp_content += "\n\n---\n# ラフ詳細\n\n"
        
        # 各ページの詳細
        pages = product_data.get('page_details', [])
        if not pages:
            # デフォルトページを生成
            pages = self._generate_default_pages(product_data)
        
        for i, page in enumerate(pages, 1):
            lp_content += f"## {i}枚目\n\n"
            
            # レイアウト案
            lp_content += "### レイアウト案\n"
            if page.get('layout_image'):
                lp_content += f"![レイアウト案]({page['layout_image']} =WxH)\n\n"
            else:
                lp_content += "【画像準備中】\n\n"
            
            if page.get('layout_note'):
                lp_content += f"{page['layout_note']}\n\n"
            
            # テキスト
            if page.get('text'):
                lp_content += "### テキスト\n\n"
                lp_content += f"{page['text']}\n\n"
            
            # 使用画像
            if page.get('images'):
                lp_content += "### 使用画像\n\n"
                for img in page['images']:
                    if img:
                        lp_content += f"{img}\n"
                    else:
                        lp_content += "【画像準備中】\n"
                lp_content += "\n"
            elif page.get('has_images', False):
                lp_content += "### 使用画像\n\n【画像準備中】\n\n"
        
        return lp_content
    
    def _generate_default_pages(self, product_data: Dict) -> List[Dict]:
        """デフォルトのページ詳細を生成"""
        pages = []
        
        # 1枚目: TOPキャッチ
        pages.append({
            'text': f"{product_data['product_name']}\n\n{product_data.get('catch_copy', 'キャッチコピーを入力してください')}\n\n{product_data.get('main_features', '')}",
            'layout_note': '商品の魅力が一目で伝わるデザインにしてください。',
            'has_images': True
        })
        
        # 2枚目: 実績・信頼性
        pages.append({
            'text': product_data.get('achievements', '販売実績・受賞歴などを記載'),
            'layout_note': '数字やロゴを効果的に配置してください。',
            'has_images': False
        })
        
        # 3枚目: ブランド価値
        pages.append({
            'text': product_data.get('brand_value', '日本ブランドとしての品質・安全性'),
            'has_images': True
        })
        
        # 4-5枚目: メイン機能
        for i in range(2):
            pages.append({
                'text': product_data.get(f'feature_{i+1}', f'特徴{i+1}の説明'),
                'has_images': True
            })
        
        # 6枚目: 使用シーン
        pages.append({
            'text': product_data.get('use_scenes', 'どこでも使える・いつでも便利'),
            'has_images': True
        })
        
        # 7-8枚目: スペック
        pages.append({
            'text': product_data.get('specs', 'サイズ・重量・仕様詳細'),
            'has_images': True
        })
        
        pages.append({
            'text': product_data.get('accessories', '付属品・同梱物一覧'),
            'has_images': True
        })
        
        # 9枚目: 保証
        pages.append({
            'text': product_data.get('warranty', '保証期間・アフターサービス'),
            'has_images': False
        })
        
        # 10枚目: FAQ
        pages.append({
            'text': product_data.get('faq', 'よくある質問と回答'),
            'has_images': False
        })
        
        return pages
    
    def save_lp_rough(self, content: str, product_name: str) -> str:
        """LPラフ案を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"lp_rough_{product_name}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def load_template(self, template_name: str) -> Dict:
        """テンプレートを読み込み"""
        template_path = os.path.join(self.template_dir, f"{template_name}.json")
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_template(self, product_data: Dict, template_name: str):
        """テンプレートとして保存"""
        template_path = os.path.join(self.template_dir, f"{template_name}.json")
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)


def interactive_input():
    """対話式入力"""
    print("\n🚀 LPラフ案自動生成システム")
    print("=" * 50)
    
    generator = LPRoughGenerator()
    
    # 起動モード選択
    print("\n起動モードを選択してください:")
    print("1. 新規作成")
    print("2. テンプレートから作成")
    print("3. JSONファイルから読み込み")
    
    mode = input("\n選択 (1-3): ").strip()
    
    product_data = {}
    
    if mode == '2':
        # テンプレート一覧表示
        templates = os.listdir(generator.template_dir)
        json_templates = [f for f in templates if f.endswith('.json')]
        
        if json_templates:
            print("\n利用可能なテンプレート:")
            for i, template in enumerate(json_templates, 1):
                print(f"{i}. {template.replace('.json', '')}")
            
            choice = input("\nテンプレート番号を選択: ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(json_templates):
                    template_name = json_templates[idx].replace('.json', '')
                    product_data = generator.load_template(template_name)
                    print(f"✅ テンプレート '{template_name}' を読み込みました")
            except:
                print("無効な選択です。新規作成モードで続行します。")
    
    elif mode == '3':
        json_path = input("\nJSONファイルのパスを入力: ").strip()
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)
            print("✅ JSONファイルを読み込みました")
        else:
            print("ファイルが見つかりません。新規作成モードで続行します。")
    
    # 必須項目の入力
    print("\n📝 商品情報を入力してください")
    print("-" * 40)
    
    if not product_data.get('product_name'):
        product_data['product_name'] = input("商品名 (必須): ").strip()
    
    if not product_data.get('purpose'):
        product_data['purpose'] = input("作成の目的・意図: ").strip() or "ECサイトでの販売促進"
    
    if not product_data.get('target_platform'):
        product_data['target_platform'] = input("対象プラットフォーム (例: 楽天以外のECサイト): ").strip() or "全ECサイト"
    
    # SKU/JAN情報
    if not product_data.get('sku_list'):
        print("\nSKU/JAN情報を入力 (スキップする場合はEnter)")
        sku_list = []
        while True:
            sku_type = input("  種類/カラー (終了はEnter): ").strip()
            if not sku_type:
                break
            sku = input("  SKU: ").strip()
            jan = input("  JAN: ").strip()
            sku_list.append({'type': sku_type, 'sku': sku, 'jan': jan})
        
        if sku_list:
            product_data['sku_list'] = sku_list
    
    # オプション項目
    if not product_data.get('catch_copy'):
        product_data['catch_copy'] = input("\nキャッチコピー: ").strip()
    
    if not product_data.get('main_features'):
        product_data['main_features'] = input("メイン機能・特徴 (簡潔に): ").strip()
    
    if not product_data.get('tonmana_url'):
        product_data['tonmana_url'] = input("トンマナ参照URL (任意): ").strip()
    
    if not product_data.get('base_data_url'):
        product_data['base_data_url'] = input("ベースデータURL (任意): ").strip()
    
    # LP構成のカスタマイズ
    customize = input("\nLP構成をカスタマイズしますか？ (y/N): ").strip().lower()
    if customize == 'y':
        print("\n各ページのコンテンツ概要を入力 (終了はEnter)")
        lp_structure = []
        page_num = 1
        while True:
            content = input(f"{page_num}枚目: ").strip()
            if not content:
                break
            lp_structure.append(content)
            page_num += 1
        
        if lp_structure:
            product_data['lp_structure'] = lp_structure
    
    # LP生成
    print("\n⚙️ LPラフ案を生成中...")
    try:
        lp_content = generator.generate_lp_rough(product_data)
        
        # プレビュー
        print("\n" + "=" * 50)
        print("📄 生成されたLPラフ案 (プレビュー)")
        print("=" * 50)
        print(lp_content[:1000] + "...\n")
        
        # 保存
        filepath = generator.save_lp_rough(lp_content, product_data['product_name'])
        print(f"✅ LPラフ案を保存しました: {filepath}")
        
        # テンプレート保存
        save_template = input("\nこの設定をテンプレートとして保存しますか？ (y/N): ").strip().lower()
        if save_template == 'y':
            template_name = input("テンプレート名: ").strip()
            if template_name:
                generator.save_template(product_data, template_name)
                print(f"✅ テンプレート '{template_name}' を保存しました")
        
        # Docbaseアップロード確認
        upload = input("\nDocbaseにアップロードしますか？ (y/N): ").strip().lower()
        if upload == 'y':
            print("\n📤 Docbaseアップロード機能を起動...")
            os.system(f"python docbase_lp_uploader.py {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # コマンドライン引数でJSONファイルを指定
        json_path = sys.argv[1]
        if os.path.exists(json_path):
            generator = LPRoughGenerator()
            with open(json_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)
            
            lp_content = generator.generate_lp_rough(product_data)
            filepath = generator.save_lp_rough(lp_content, product_data['product_name'])
            print(f"✅ LPラフ案を生成しました: {filepath}")
        else:
            print(f"❌ ファイルが見つかりません: {json_path}")
    else:
        # 対話式モード
        interactive_input()