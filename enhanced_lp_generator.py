#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精度向上版LPラフ案生成システム
"""

from typing import Dict, Any, List
from datetime import datetime

class EnhancedLPGenerator:
    def __init__(self):
        """初期化"""
        # ページ構成テンプレート
        self.page_structures = {
            'electronics': [
                'TOPキャッチ・商品紹介',
                'ブランド価値・信頼性', 
                'メイン機能・特徴1',
                'メイン機能・特徴2',
                '使用シーン・ライフスタイル',
                'サイズ・スペック詳細',
                'カラーバリエーション',
                '安全機能・品質保証',
                'よくある質問',
                '購入特典・販売店情報'
            ],
            'outdoor': [
                'TOPキャッチ・アウトドア訴求',
                'ブランド×アウトドア体験',
                'アウトドア特化機能',
                '耐久性・実用性',
                'キャンプシーン・使用例',
                'スペック・携帯性',
                'カラー・デザイン',
                '安全性・メンテナンス',
                'ユーザーレビュー',
                '購入・アフターサービス'
            ],
            'lifestyle': [
                'TOPキャッチ・ライフスタイル提案',
                'ブランドストーリー',
                'ライフスタイル向上機能',
                'デザイン・インテリア性',
                '日常使用シーン',
                'サイズ・使いやすさ',
                'カラー・バリエーション',
                '品質・保証',
                'ユーザー体験談',
                '購入方法・特典'
            ]
        }
        
        # 画像指示テンプレート
        self.image_templates = {
            'main_product': '商品メイン画像：白背景、正面、高品質',
            'lifestyle': 'ライフスタイル画像：実際の使用シーン、自然光',
            'detail': '詳細画像：機能部分のクローズアップ、説明文付き',
            'comparison': '比較画像：サイズ感、他商品との差別化',
            'scene': 'シーン画像：使用環境、ユーザー行動',
            'spec': 'スペック画像：寸法図、仕様表、認証マーク',
            'color': 'カラー画像：全色並列、テクスチャ感',
            'brand': 'ブランド画像：ロゴ、ブランドイメージ'
        }
    
    def analyze_product_category(self, product_data: Dict) -> str:
        """商品カテゴリを分析"""
        product_name = product_data.get('product_name', '').lower()
        features = ' '.join(product_data.get('main_features', [])).lower()
        description = str(product_data.get('purpose', '')).lower()
        
        # キーワードベースでカテゴリ判定
        if any(word in product_name + features + description for word in 
               ['camp', 'outdoor', 'アウトドア', 'キャンプ', 'powerarq']):
            return 'outdoor'
        elif any(word in product_name + features + description for word in 
                 ['electric', 'electronic', '電気', '電子', 'スマート', 'デジタル']):
            return 'electronics'
        else:
            return 'lifestyle'
    
    def generate_enhanced_page_content(self, page_num: int, page_title: str, 
                                     product_data: Dict, category: str) -> Dict:
        """強化されたページコンテンツ生成"""
        
        product_name = product_data.get('product_name', '')
        features = product_data.get('main_features', [])
        specs = product_data.get('specifications', {})
        
        # ページ別のコンテンツ生成
        if page_num == 1:  # TOPキャッチ
            return self._generate_top_page(product_name, features, category)
        elif page_num == 2:  # ブランド価値
            return self._generate_brand_page(product_data, category)
        elif page_num == 3:  # メイン機能1
            return self._generate_feature_page(features, 0, category)
        elif page_num == 4:  # メイン機能2
            return self._generate_feature_page(features, 1, category)
        elif page_num == 5:  # 使用シーン
            return self._generate_scene_page(product_data, category)
        elif page_num == 6:  # スペック
            return self._generate_spec_page(specs, category)
        elif page_num == 7:  # カラー
            return self._generate_color_page(product_data, category)
        elif page_num == 8:  # 安全・品質
            return self._generate_safety_page(product_data, category)
        elif page_num == 9:  # FAQ
            return self._generate_faq_page(product_data, category)
        elif page_num == 10:  # 購入・特典
            return self._generate_purchase_page(product_data, category)
        else:
            return self._generate_default_page(page_title, product_data)
    
    def _generate_top_page(self, product_name: str, features: List, category: str) -> Dict:
        """TOPページ生成"""
        if category == 'outdoor':
            text = f'{product_name}\\n\\nアウトドアライフを変える\\n\\n'
        elif category == 'electronics':
            text = f'{product_name}\\n\\n先進技術で暮らしをスマートに\\n\\n'
        else:
            text = f'{product_name}\\n\\n新しいライフスタイルを提案\\n\\n'
        
        # 主要機能を3つまで表示
        for i, feature in enumerate(features[:3]):
            text += f'• {feature}\\n'
        
        return {
            'text': text,
            'layout_note': 'インパクトのあるメインビジュアル、商品の魅力を一目で伝える構成',
            'image_instruction': self.image_templates['main_product'],
            'design_priority': 'high',
            'has_images': True
        }
    
    def _generate_brand_page(self, product_data: Dict, category: str) -> Dict:
        """ブランドページ生成"""
        brand_value = product_data.get('brand_value', '')
        
        if category == 'outdoor':
            text = f'{brand_value}\\n\\nアウトドア専用設計\\n\\n信頼のブランドが提案する\\n新しいアウトドア体験'
        else:
            text = f'{brand_value}\\n\\n品質への こだわり\\n\\n長年の実績と技術力で\\nお客様の信頼にお応え'
        
        return {
            'text': text,
            'layout_note': 'ブランドロゴを大きく、実績数値を効果的に配置',
            'image_instruction': self.image_templates['brand'],
            'design_priority': 'medium',
            'has_images': True
        }
    
    def _generate_feature_page(self, features: List, index: int, category: str) -> Dict:
        """機能ページ生成"""
        if index < len(features):
            feature = features[index]
            if category == 'outdoor':
                text = f'{feature}\\n\\nフィールドでの実用性を追求\\n\\n過酷な環境でも確実に動作'
            else:
                text = f'{feature}\\n\\n使いやすさを追求した設計\\n\\n毎日の生活がもっと便利に'
        else:
            text = '高性能機能搭載\\n\\n快適な使用体験を\\nお届けします'
        
        return {
            'text': text,
            'layout_note': '機能の動作イメージ、使用前後の比較',
            'image_instruction': self.image_templates['detail'],
            'design_priority': 'high',
            'has_images': True
        }
    
    def _generate_scene_page(self, product_data: Dict, category: str) -> Dict:
        """使用シーンページ生成"""
        scenes = product_data.get('usage_scenes', [])
        
        if category == 'outdoor':
            text = 'あらゆるアウトドアシーンで\\n\\nキャンプ・登山・車中泊\\nどこでも活躍'
        else:
            text = 'いつでも、どこでも\\n\\nリビング・寝室・オフィス\\nあらゆるシーンで活躍'
        
        if scenes:
            text += '\\n\\n' + '・'.join(scenes)
        
        return {
            'text': text,
            'layout_note': '複数の使用シーンを並べたコラージュ風レイアウト',
            'image_instruction': self.image_templates['scene'],
            'design_priority': 'medium',
            'has_images': True
        }
    
    def _generate_spec_page(self, specs: Dict, category: str) -> Dict:
        """スペックページ生成"""
        text = '仕様・スペック\\n\\n'
        
        # 主要スペックを抽出
        for key, value in specs.items():
            text += f'{key}：{value}\\n'
        
        return {
            'text': text,
            'layout_note': '見やすいスペック表、サイズ感の比較画像',
            'image_instruction': self.image_templates['spec'],
            'design_priority': 'medium',
            'has_images': True
        }
    
    def _generate_color_page(self, product_data: Dict, category: str) -> Dict:
        """カラーページ生成"""
        colors = product_data.get('design_variants', [])
        
        text = 'カラーバリエーション\\n\\n'
        if colors:
            text += f'{" / ".join(colors)}\\n\\nお好みに合わせてお選びください'
        else:
            text += '豊富なカラー展開\\n\\nライフスタイルに合わせて'
        
        return {
            'text': text,
            'layout_note': '全カラーを美しく並べた比較レイアウト',
            'image_instruction': self.image_templates['color'],
            'design_priority': 'medium',
            'has_images': True
        }
    
    def _generate_safety_page(self, product_data: Dict, category: str) -> Dict:
        """安全・品質ページ生成"""
        specs = product_data.get('specifications', {})
        safety_features = [v for k, v in specs.items() if '安全' in k or '保護' in k]
        
        text = '安全機能・品質保証\\n\\n'
        if safety_features:
            for feature in safety_features:
                text += f'• {feature}\\n'
        else:
            text += '徹底した品質管理\\n安心してお使いいただけます'
        
        return {
            'text': text,
            'layout_note': '安全認証マーク、品質テストの様子',
            'image_instruction': '安全機能の説明図、認証マーク、品質テスト画像',
            'design_priority': 'medium',
            'has_images': True
        }
    
    def _generate_faq_page(self, product_data: Dict, category: str) -> Dict:
        """FAQページ生成"""
        if category == 'outdoor':
            text = 'よくある質問\\n\\nQ: アウトドアで使えますか？\\nA: はい、屋外での使用を想定した設計です\\n\\nQ: メンテナンスは？\\nA: 簡単なお手入れで長くお使いいただけます'
        elif category == 'electronics':
            text = 'よくある質問\\n\\nQ: 電力消費はどのくらい？\\nA: 省エネ設計で電気代を抑えます\\n\\nQ: 操作は簡単？\\nA: 直感的な操作で誰でも簡単に使えます'
        else:
            text = 'よくある質問\\n\\nQ: お手入れは簡単？\\nA: 日常的なお手入れで清潔に保てます\\n\\nQ: 保証期間は？\\nA: 安心の品質保証付きです'
        
        return {
            'text': text,
            'layout_note': 'Q&A形式で見やすく、重要な質問を優先',
            'image_instruction': 'FAQ関連の説明画像、使い方ガイド',
            'design_priority': 'low',
            'has_images': False
        }
    
    def _generate_purchase_page(self, product_data: Dict, category: str) -> Dict:
        """購入ページ生成"""
        price = product_data.get('price', '価格調整中')
        
        text = f'今すぐお得に購入\\n\\n{price}\\n\\n送料無料\\n品質保証付き'
        
        return {
            'text': text,
            'layout_note': '購入ボタンを大きく、特典を分かりやすく',
            'image_instruction': '特典内容、購入方法の説明画像',
            'design_priority': 'high',
            'has_images': True
        }
    
    def _generate_default_page(self, page_title: str, product_data: Dict) -> Dict:
        """デフォルトページ生成"""
        return {
            'text': f'{page_title}\\n\\n詳細情報を\\n記載してください',
            'layout_note': 'コンテンツに応じたレイアウト',
            'image_instruction': '【画像準備中】',
            'design_priority': 'medium',
            'has_images': True
        }
    
    def generate_enhanced_lp_rough(self, product_data: Dict) -> str:
        """強化版LPラフ案生成"""
        
        # 商品カテゴリ分析
        category = self.analyze_product_category(product_data)
        
        # カテゴリに応じたページ構成取得
        page_structure = self.page_structures.get(category, self.page_structures['lifestyle'])
        
        # 基本情報
        product_name = product_data.get('product_name', '商品名')
        purpose = product_data.get('purpose', '販売促進のため')
        
        # LPラフ案開始
        lp_content = f"""# LPラフ（強化版）
## 作成の目的、意図
{purpose}

## 商品カテゴリ分析
カテゴリ: {category}
適用構成: {category}向け最適化

## 対象商品
### 商品名
{product_name}

### SKU・JAN
| 種類 | SKU | JAN |
| --- | --- | --- |
"""
        
        # SKU情報追加
        sku_list = product_data.get('sku_list', [])
        for sku in sku_list:
            lp_content += f"| {sku.get('type', '')} | {sku.get('sku', '')} | {sku.get('jan', '')} |\n"
        
        if not sku_list:
            lp_content += "| カラー/サイズ | SKUコード | JANコード |\n"
        
        # 基本情報セクション
        lp_content += """
## 基本情報
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
トンマナに関しては別途共有します。

### 画像指示システム
- **優先度**: high（最重要）/ medium（重要）/ low（補助）
- **画像種別**: メイン商品/ライフスタイル/詳細/比較/シーン/スペック/カラー/ブランド
- **指示内容**: 具体的な撮影・制作指示

---
# LP構成（{category}最適化版）
| 枚数 | コンテンツ概要 | 優先度 |
| --- | --- | --- |
"""
        
        # ページ構成テーブル
        for i, page_title in enumerate(page_structure, 1):
            page_content = self.generate_enhanced_page_content(i, page_title, product_data, category)
            priority = page_content.get('design_priority', 'medium')
            lp_content += f"| {i}枚目 | {page_title} | {priority} |\n"
        
        # 詳細ページセクション
        lp_content += "\n\n---\n# ラフ詳細（強化版）\n\n"
        
        for i, page_title in enumerate(page_structure, 1):
            page_content = self.generate_enhanced_page_content(i, page_title, product_data, category)
            
            lp_content += f"""## {i}枚目 - {page_title}

### 📸 画像指示（優先度: {page_content.get('design_priority', 'medium')}）
{page_content.get('image_instruction', '【画像準備中】')}

### 🎨 レイアウト案
{page_content.get('layout_note', 'コンテンツに応じたレイアウト')}

### ✏️ テキスト
{page_content.get('text', 'テキスト内容')}

### 🖼️ 使用画像
{"画像あり" if page_content.get('has_images') else "画像なし"}

---

"""
        
        # 制作ガイドライン追加
        lp_content += """
# 🎯 制作ガイドライン

## 画像制作指示
### 最重要（high priority）
1枚目、3枚目、4枚目、10枚目 - メインビジュアル、機能訴求、購入訴求

### 重要（medium priority）  
2枚目、5枚目、6枚目、7枚目、8枚目 - ブランド、シーン、スペック、カラー、安全性

### 補助（low priority）
9枚目 - FAQ（テキスト中心）

## デザイン方針
- **統一感**: ブランドカラーとトーンを統一
- **視認性**: 文字の可読性を最優先
- **訴求力**: 商品の魅力を視覚的に表現
- **信頼感**: 品質感のあるデザイン

## レスポンシブ対応
- PC版（1200px）をベースデザイン
- SP版（850px）で最適化
- Flick版（1000px）でタブレット対応
"""
        
        return lp_content