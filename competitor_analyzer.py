#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
競合分析・他社事例参照システム
"""

import os
import re
import json
import requests
from typing import Dict, Any, List
from datetime import datetime
from urllib.parse import urljoin, urlparse

class CompetitorAnalyzer:
    def __init__(self):
        """初期化"""
        # 分析対象サイト（例：家電・アウトドア関連）
        self.target_sites = {
            'rakuten': {
                'base_url': 'https://search.rakuten.co.jp/search/mall/',
                'selectors': {
                    'title': '.dui-cards .itemName',
                    'price': '.important',
                    'features': '.itemCaption'
                }
            },
            'amazon': {
                'base_url': 'https://www.amazon.co.jp/s?k=',
                'selectors': {
                    'title': '[data-component-type="s-search-result"] h2',
                    'price': '.a-price .a-offscreen',
                    'features': '.a-size-base'
                }
            },
            'yodobashi': {
                'base_url': 'https://www.yodobashi.com/category/',
                'selectors': {
                    'title': '.pName',
                    'price': '.pPrice',
                    'features': '.pSpec'
                }
            }
        }
        
        # 成功パターンライブラリ
        self.success_patterns = {
            'electronics': {
                'key_appeals': ['省エネ', '高性能', '簡単操作', '安全性', '長期保証'],
                'structure_priority': ['機能訴求', '価格競争力', 'ブランド信頼性', '使いやすさ'],
                'copy_patterns': ['○段階', '自動○○', '○○対応', '○○機能付き']
            },
            'outdoor': {
                'key_appeals': ['軽量', '防水', '耐久性', 'コンパクト', 'アウトドア専用'],
                'structure_priority': ['実用性', 'ポータビリティ', '環境対応', 'ブランド実績'],
                'copy_patterns': ['○○対応', '軽量○kg', '防水IP○○', 'アウトドア○○']
            },
            'lifestyle': {
                'key_appeals': ['デザイン性', 'インテリア', '健康', '快適性', 'ライフスタイル'],
                'structure_priority': ['ライフスタイル提案', 'デザイン性', '快適性', '価格'],
                'copy_patterns': ['○○な暮らし', '毎日○○', 'ライフスタイル○○']
            }
        }
    
    def analyze_similar_products(self, product_name: str, category: str = 'electronics') -> Dict[str, Any]:
        """類似商品の分析を実行"""
        
        print(f"📊 競合分析開始: {product_name} (カテゴリ: {category})")
        
        # 検索キーワード生成
        search_keywords = self._generate_search_keywords(product_name)
        print(f"🔍 検索キーワード: {search_keywords}")
        
        # 競合商品情報収集（サンプル）
        competitor_data = self._collect_competitor_data(search_keywords)
        
        # ベストプラクティス分析
        best_practices = self._analyze_best_practices(competitor_data, category)
        
        # 訴求ポイント最適化
        optimized_appeals = self._optimize_appeals(product_name, best_practices, category)
        
        result = {
            'search_keywords': search_keywords,
            'competitor_count': len(competitor_data),
            'competitor_data': competitor_data,
            'best_practices': best_practices,
            'optimized_appeals': optimized_appeals,
            'recommendations': self._generate_recommendations(best_practices, category),
            'analysis_date': datetime.now().isoformat()
        }
        
        print(f"✅ 競合分析完了: {len(competitor_data)}商品を分析")
        return result
    
    def _generate_search_keywords(self, product_name: str) -> List[str]:
        """検索キーワードを生成"""
        
        # 商品名から重要キーワード抽出
        keywords = []
        
        # 基本的なキーワード抽出
        base_keywords = product_name.replace(' ', '').split()
        for keyword in base_keywords:
            if len(keyword) > 1:
                keywords.append(keyword)
        
        # 特定商品の場合の専用キーワード
        if 'Electric Blanket' in product_name or '電気毛布' in product_name:
            keywords.extend(['電気毛布', '電気ブランケット', '電気ひざ掛け', '発熱毛布'])
        
        if 'PowerArQ' in product_name:
            keywords.extend(['ポータブル電源', 'アウトドア電源', 'キャンプ電源'])
        
        return list(set(keywords))
    
    def _collect_competitor_data(self, keywords: List[str]) -> List[Dict]:
        """競合データ収集（サンプル実装）"""
        
        # 実際の実装では Web Scraping や API を使用
        # ここではサンプルデータを返す
        sample_data = [
            {
                'product_name': '山善 電気毛布 掛け敷き両用',
                'price': '3,980円',
                'key_features': ['洗濯機丸洗いOK', 'ダニ退治機能', '室温センサー付き'],
                'appeal_points': ['安心の日本メーカー', '5段階温度調節', 'PSEマーク取得'],
                'page_structure': ['商品画像', 'キャッチコピー', '機能説明', '安全性', '価格'],
                'ranking': '電気毛布ランキング1位',
                'review_score': 4.3,
                'review_count': 1250
            },
            {
                'product_name': 'コイズミ 電気毛布 KDK-L105',
                'price': '2,580円',
                'key_features': ['省エネ', '頭寒足熱配線', '抗菌防臭加工'],
                'appeal_points': ['電気代約1.4円/時間', '8段階温度調節', '安心の2年保証'],
                'page_structure': ['省エネアピール', '機能詳細', '使用シーン', '価格比較'],
                'ranking': '電気毛布ランキング3位',
                'review_score': 4.1,
                'review_count': 890
            },
            {
                'product_name': 'パナソニック 電気かけしき毛布',
                'price': '8,980円',
                'key_features': ['自動温度調節', 'マイクロファイバー', '速暖性'],
                'appeal_points': ['パナソニック品質', '快適自動制御', '肌触り抜群'],
                'page_structure': ['ブランド訴求', '高級感', '技術力', '快適性'],
                'ranking': '高級電気毛布部門1位',
                'review_score': 4.6,
                'review_count': 445
            }
        ]
        
        return sample_data
    
    def _analyze_best_practices(self, competitor_data: List[Dict], category: str) -> Dict[str, Any]:
        """ベストプラクティス分析"""
        
        # 共通成功パターンを抽出
        common_appeals = {}
        common_structures = {}
        price_ranges = []
        high_rated_features = []
        
        for product in competitor_data:
            # 訴求ポイントの集計
            for appeal in product.get('appeal_points', []):
                common_appeals[appeal] = common_appeals.get(appeal, 0) + 1
            
            # ページ構成の集計
            for structure in product.get('page_structure', []):
                common_structures[structure] = common_structures.get(structure, 0) + 1
            
            # 価格レンジ
            price_str = product.get('price', '0円')
            price_num = int(re.sub(r'[^\d]', '', price_str))
            if price_num > 0:
                price_ranges.append(price_num)
            
            # 高評価商品の特徴
            if product.get('review_score', 0) >= 4.0:
                high_rated_features.extend(product.get('key_features', []))
        
        # ベストプラクティス
        best_practices = {
            'top_appeals': sorted(common_appeals.items(), key=lambda x: x[1], reverse=True)[:5],
            'effective_structures': sorted(common_structures.items(), key=lambda x: x[1], reverse=True)[:5],
            'price_range': {
                'min': min(price_ranges) if price_ranges else 0,
                'max': max(price_ranges) if price_ranges else 0,
                'avg': sum(price_ranges) // len(price_ranges) if price_ranges else 0
            },
            'success_features': list(set(high_rated_features)),
            'category_trends': self.success_patterns.get(category, {})
        }
        
        return best_practices
    
    def _optimize_appeals(self, product_name: str, best_practices: Dict, category: str) -> List[str]:
        """訴求ポイントの最適化"""
        
        optimized = []
        
        # トップ訴求ポイントから適用可能なものを選択
        top_appeals = [appeal[0] for appeal in best_practices.get('top_appeals', [])]
        
        # PowerArQ Electric Blanket Liteの場合の最適化
        if 'Electric Blanket' in product_name:
            # 温度調節系の訴求
            if any('段階' in appeal for appeal in top_appeals):
                optimized.append('10段階の細かい温度調節で最適な暖かさ')
            
            # 安全性系の訴求
            if any('安全' in appeal or '安心' in appeal for appeal in top_appeals):
                optimized.append('過熱保護システム搭載で安心・安全')
            
            # ブランド系の訴求
            if any('メーカー' in appeal or 'ブランド' in appeal for appeal in top_appeals):
                optimized.append('PowerARQブランドの信頼性と品質')
            
            # 使いやすさ系
            if any('簡単' in appeal or '操作' in appeal for appeal in top_appeals):
                optimized.append('コントローラーで簡単操作')
            
            # アウトドア特化（PowerArQの強み）
            optimized.append('キャンプ・アウトドアに最適なデザイン')
        
        # カテゴリ固有の最適化
        category_patterns = self.success_patterns.get(category, {})
        if category_patterns:
            for pattern in category_patterns.get('key_appeals', [])[:3]:
                if pattern not in ' '.join(optimized):
                    optimized.append(f'{pattern}を重視した設計')
        
        return optimized[:6]  # 最大6つまで
    
    def _generate_recommendations(self, best_practices: Dict, category: str) -> Dict[str, List]:
        """改善提案生成"""
        
        recommendations = {
            'page_structure': [],
            'copy_improvements': [],
            'pricing_strategy': [],
            'feature_emphasis': []
        }
        
        # ページ構成の提案
        effective_structures = [s[0] for s in best_practices.get('effective_structures', [])]
        recommendations['page_structure'] = [
            f"{structure}を強調したページを追加することを推奨" 
            for structure in effective_structures[:3]
        ]
        
        # コピー改善提案
        success_features = best_practices.get('success_features', [])
        recommendations['copy_improvements'] = [
            "競合の成功パターンを参考に訴求ポイントを強調",
            "競合との差別化ポイントを明確化", 
            "数値的な根拠（○段階、○時間等）を活用"
        ]
        
        # 成功特徴がある場合は具体的に追加
        if success_features:
            recommendations['copy_improvements'].insert(0, f"「{success_features[0]}」を訴求ポイントとして強調")
        
        # 価格戦略
        price_range = best_practices.get('price_range', {})
        if price_range.get('avg', 0) > 0:
            recommendations['pricing_strategy'] = [
                f"市場平均価格: {price_range['avg']:,}円",
                f"価格レンジ: {price_range['min']:,}円 〜 {price_range['max']:,}円",
                "価格競争力または付加価値の訴求が重要"
            ]
        
        # 機能強調提案
        recommendations['feature_emphasis'] = success_features[:5]
        
        return recommendations
    
    def generate_enhanced_lp_with_analysis(self, product_data: Dict, competitor_analysis: Dict) -> str:
        """競合分析を反映した強化LPラフ案生成"""
        
        optimized_appeals = competitor_analysis.get('optimized_appeals', [])
        recommendations = competitor_analysis.get('recommendations', {})
        best_practices = competitor_analysis.get('best_practices', {})
        
        # 基本情報
        product_name = product_data.get('商品名', '')
        
        # 競合分析を反映したLPラフ案
        enhanced_lp = f"""# LPラフ（競合分析強化版）

## 📊 競合分析サマリー
- 分析商品数: {competitor_analysis.get('competitor_count', 0)}商品
- 市場平均価格: {best_practices.get('price_range', {}).get('avg', 0):,}円
- 成功パターン: {len(best_practices.get('success_features', []))}の共通特徴を確認

## 作成の目的、意図
{product_data.get('purpose', '販売促進のため')}

**💡 競合分析による改善点:**
{chr(10).join([f'• {rec}' for rec in recommendations.get('copy_improvements', [])[:3]])}

## 対象商品
### 商品名
{product_name}

### 🎯 最適化された訴求ポイント
{chr(10).join([f'• {appeal}' for appeal in optimized_appeals[:5]])}

### SKU・JAN
| 種類 | SKU | JAN |
| --- | --- | --- |
"""
        
        # SKU情報
        sku_list = product_data.get('sku_list', [])
        if sku_list:
            for sku in sku_list:
                enhanced_lp += f"| {sku.get('type', '')} | {sku.get('sku', '')} | {sku.get('jan', '')} |\n"
        else:
            enhanced_lp += "| カラー・サイズ | SKUコード | JANコード |\n"
        
        # 競合分析を反映したLP構成
        enhanced_lp += f"""
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

---
# LP構成（競合分析最適化版）

## 📈 成功パターンに基づく構成
{chr(10).join([f'• {pattern[0]} (競合{pattern[1]}社で使用)' for pattern in best_practices.get('effective_structures', [])[:5]])}

| 枚数 | コンテンツ概要 | 競合分析ポイント |
| --- | --- | --- |
| 1枚目 | TOPキャッチ | 最適化された訴求ポイントを使用 |
| 2枚目 | 売れている訴求・実績 | 競合の実績訴求パターンを参考 |
| 3枚目 | ブランド価値・差別化 | 競合との明確な差別化点 |
| 4枚目 | メイン機能1（温度調節） | 「○段階調節」の訴求パターン活用 |
| 5枚目 | メイン機能2（安全性） | 競合で成功している「安心・安全」訴求 |
| 6枚目 | 使用シーン・ライフスタイル | アウトドア特化の差別化 |
| 7枚目 | サイズ・スペック詳細 | 競合比較を意識した情報提示 |
| 8枚目 | 付属品・同梱物 | 競合に対する優位点を強調 |
| 9枚目 | 保証・アフターサービス | 競合の保証期間を上回る提案 |
| 10枚目 | よくある質問・競合比較 | 競合選定理由への回答 |

---
# ラフ詳細（競合分析強化版）

## 1枚目 - TOPキャッチ（最適化版）

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: トップ訴求「{optimized_appeals[0] if optimized_appeals else '温度調節'}」を最大に活用

### テキスト
{product_name}

{optimized_appeals[0] if optimized_appeals else '快適な温もりを'}

• {optimized_appeals[1] if len(optimized_appeals) > 1 else '高機能'}
• {optimized_appeals[2] if len(optimized_appeals) > 2 else '安全設計'}
• アウトドア特化設計（競合差別化点）

### 使用画像
【画像準備中】

## 2枚目 - 実績訴求（競合対抗版）

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: {best_practices.get('top_appeals', [('実績訴求', 1)])[0][0]}パターンを採用

### テキスト
PowerARQブランドの実績

✨ アウトドア電源分野での圧倒的実績
📊 累計販売台数○○万台突破
🏆 アウトドア専門誌で高評価獲得

💡 **競合優位点**: 一般家電メーカーにない「アウトドア専用設計」

## 3枚目 - 差別化・ブランド価値

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: 競合の弱点「アウトドア対応不足」を突く

### テキスト
なぜPowerArQ Electric Blanket Liteなのか？

🏕️ **アウトドア専用設計**
一般的な家庭用電気毛布では実現できない、キャンプ・アウトドア環境での使用を前提とした設計

⚡ **ポータブル電源との親和性**
PowerARQ製品との組み合わせで、どこでも快適な温もり環境を実現

### 使用画像
【画像準備中】

## 4枚目 - メイン機能1（10段階温度調節）

### レイアウ案
【画像準備中】

🎯 **競合分析ポイント**: 「{best_practices.get('success_features', ['温度調節'])[0]}」成功パターン活用

### テキスト
10段階の細かい温度調節

🌡️ **他社比較**
• A社: 5段階調節
• B社: 8段階調節  
• PowerArQ: **10段階調節**（業界最高レベル）

体調や環境に合わせて、1°C単位での細かい調整が可能

### 使用画像
【画像準備中】

## 5枚目 - メイン機能2（安全性・過熱保護）

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: 「安心・安全」訴求パターンを強化

### テキスト
過熱保護システム搭載

🛡️ **安全機能**
• 自動電源OFF機能
• 温度異常検知システム
• 電磁波カット技術
• PSE認証取得済み

安全性において競合他社を上回る充実した保護機能

### 使用画像
【画像準備中】

## 6枚目 - 使用シーン（アウトドア特化）

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: アウトドア特化による差別化

### テキスト
キャンプ・アウトドアでの使用シーン

🏕️ **活用場面**
• テント内での就寝時
• 焚き火タイムの膝掛け
• 車中泊での防寒対策
• 釣りやBBQでの体温保持

家庭用とは違う、本格アウトドア仕様

### 使用画像
【画像準備中】

## 7枚目 - スペック詳細（競合比較）

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: 他社との機能比較表で優位性明示

### テキスト
詳細スペック・競合比較

📊 **他社比較表**
| 項目 | PowerArQ | A社 | B社 |
|-----|---------|-----|-----|
| 温度調節 | 10段階 | 5段階 | 8段階 |
| 過熱保護 | ◎ | ○ | △ |
| アウトドア対応 | ◎ | × | × |
| ポータブル電源対応 | ◎ | × | △ |

### 使用画像
【画像準備中】

## 8枚目 - 付属品・同梱物

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: 充実の付属品でお得感演出

### テキスト
充実の付属品セット

📦 **同梱内容**
• 電気毛布本体
• 専用コントローラー
• 収納バッグ
• 取扱説明書
• 保証書

他社では別売りの収納バッグが標準付属

### 使用画像
【画像準備中】

## 9枚目 - 保証・アフターサービス

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: 手厚いサポートで購入後の安心感

### テキスト
充実の保証・サポート体制

🛡️ **保証内容**
• メーカー保証1年
• 故障時の無料修理
• 部品交換対応
• 全国対応サポートセンター

### サポート連絡先
PowerARQサポートセンター
TEL: 03-xxxx-xxxx
Email: support@powerarq.jp

### 使用画像
【画像準備中】

## 10枚目 - よくある質問・購入決定

### レイアウト案
【画像準備中】

🎯 **競合分析ポイント**: 他社比較質問で購入理由を明確化

### テキスト
よくある質問

**Q1: 他社製品との違いは？**
A1: アウトドア専用設計と10段階温度調節が最大の特徴です

**Q2: ポータブル電源での使用時間は？**
A2: PowerArQ Pro(1000Wh)で約8-10時間の連続使用が可能

**Q3: 洗濯は可能ですか？**
A3: 手洗い可能です（洗濯機不可）

**Q4: 価格が他社より高い理由は？**
A4: アウトドア特化設計と品質へのこだわりによる適正価格です

### 購入ボタン
【今すぐ購入する】

### 使用画像
【画像準備中】

## 競合分析データ
"""
        
        # 競合分析の詳細データも追加
        enhanced_lp += f"""
### 📊 市場分析データ
- **価格競争力**: 市場平均{best_practices.get('price_range', {}).get('avg', 0):,}円に対する位置づけ
- **機能優位性**: {len(best_practices.get('success_features', []))}項目で競合優位
- **差別化ポイント**: アウトドア特化（競合にない強み）

### 🎯 推奨改善点
{chr(10).join([f'• {rec}' for rec in recommendations.get('page_structure', [])[:3]])}

### 📈 期待効果
- 競合商品からの乗り換え促進
- アウトドア市場での優位性確立
- ブランド差別化の明確化
"""
        
        return enhanced_lp

def main():
    """メイン処理（テスト用）"""
    
    # サンプル商品データ
    sample_product = {
        '商品名': 'PowerArQ Electric Blanket Lite',
        'purpose': 'PowerArQ Electric Blanket Liteの販売促進とアウトドア市場でのシェア拡大',
        'sku_list': [
            {'type': 'ブラック', 'sku': 'J-OB31201-BK', 'jan': '4571427130640'},
            {'type': 'ベージュ', 'sku': 'J-OB31201-BG', 'jan': '4571427130657'}
        ]
    }
    
    # 競合分析実行
    analyzer = CompetitorAnalyzer()
    analysis = analyzer.analyze_similar_products('PowerArQ Electric Blanket Lite', 'outdoor')
    
    # 強化LPラフ案生成
    enhanced_lp = analyzer.generate_enhanced_lp_with_analysis(sample_product, analysis)
    
    # 結果保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = f'output/lp_rough_enhanced_{timestamp}.md'
    
    os.makedirs('output', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_lp)
    
    print(f"✅ 競合分析強化LP生成完了: {output_path}")
    
    # 分析結果も保存
    analysis_path = f'output/competitor_analysis_{timestamp}.json'
    with open(analysis_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"📊 競合分析データ保存: {analysis_path}")

if __name__ == "__main__":
    main()