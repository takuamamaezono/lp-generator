#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
競合分析機能付き高度LPラフ案生成システム
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any
from correct_lp_generator import CorrectLPGenerator
from competitor_analyzer import CompetitorAnalyzer
from docbase_lp_uploader import DocbaseLPUploader

class AdvancedLPGenerator(CorrectLPGenerator):
    def __init__(self):
        """初期化"""
        super().__init__()
        self.competitor_analyzer = CompetitorAnalyzer()
    
    def generate_with_competitor_analysis(self, csv_path: str, enable_analysis: bool = True, 
                                        upload_to_docbase: bool = False) -> Dict[str, Any]:
        """競合分析機能付きLPラフ案生成"""
        
        print(f"\n🚀 高度LP生成システム開始")
        print(f"📁 入力ファイル: {csv_path}")
        print(f"🔍 競合分析: {'有効' if enable_analysis else '無効'}")
        
        try:
            # 基本データ抽出
            product_data = self.parse_kishima_csv(csv_path)
            product_name = product_data.get('商品名', '商品名不明')
            print(f"✅ 商品データ抽出完了: {product_name}")
            
            result = {
                'product_data': product_data,
                'product_name': product_name,
                'analysis_enabled': enable_analysis
            }
            
            # 競合分析実行
            if enable_analysis:
                print(f"\n🔍 競合分析開始...")
                
                # 商品カテゴリ自動判定
                category = self._detect_category(product_name)
                print(f"📊 商品カテゴリ: {category}")
                
                # 競合分析実行
                competitor_analysis = self.competitor_analyzer.analyze_similar_products(
                    product_name, category
                )
                
                # 競合分析結果を統合
                result['competitor_analysis'] = competitor_analysis
                result['category'] = category
                
                print(f"✅ 競合分析完了: {competitor_analysis.get('competitor_count', 0)}商品を分析")
                
                # 強化版LPラフ案生成
                print(f"\n📝 競合分析反映LPラフ案生成中...")
                enhanced_lp_content = self.competitor_analyzer.generate_enhanced_lp_with_analysis(
                    product_data, competitor_analysis
                )
                result['lp_content'] = enhanced_lp_content
                result['generation_type'] = '競合分析強化版'
                
            else:
                # 通常版LPラフ案生成
                print(f"\n📝 通常LPラフ案生成中...")
                lp_content = self.generate_correct_lp_rough(product_data)
                result['lp_content'] = lp_content
                result['generation_type'] = '通常版'
            
            # ファイル保存
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_product_name = product_name.replace(' ', '_').replace('/', '_')
            
            # LPラフ案保存
            lp_filename = f"lp_rough_{'enhanced' if enable_analysis else 'standard'}_{safe_product_name}_{timestamp}.md"
            lp_output_path = os.path.join('output', lp_filename)
            
            os.makedirs('output', exist_ok=True)
            with open(lp_output_path, 'w', encoding='utf-8') as f:
                f.write(result['lp_content'])
            
            result['lp_output_path'] = lp_output_path
            print(f"📁 LPラフ案保存: {lp_output_path}")
            
            # 競合分析データ保存
            if enable_analysis and 'competitor_analysis' in result:
                analysis_filename = f"competitor_analysis_{safe_product_name}_{timestamp}.json"
                analysis_output_path = os.path.join('output', analysis_filename)
                
                import json
                with open(analysis_output_path, 'w', encoding='utf-8') as f:
                    json.dump(result['competitor_analysis'], f, ensure_ascii=False, indent=2)
                
                result['analysis_output_path'] = analysis_output_path
                print(f"📊 競合分析データ保存: {analysis_output_path}")
            
            # Docbaseアップロード
            if upload_to_docbase:
                try:
                    print(f"\n📤 Docbaseアップロード中...")
                    
                    # タイトルとタグ設定
                    title_prefix = "【LPラフ案・競合分析版】" if enable_analysis else "【LPラフ案】"
                    title = f"{title_prefix}{product_name}"
                    
                    tags = ['LPラフ案']
                    if enable_analysis:
                        tags.extend(['競合分析', '市場調査', '最適化'])
                        if 'category' in result:
                            tags.append(result['category'])
                    
                    if 'PowerArQ' in product_name:
                        tags.extend(['PowerArQ', '電気毛布', 'アウトドア'])
                    
                    # アップロード実行
                    docbase_result = self.docbase_uploader.create_lp_post(
                        title, result['lp_content'], tags
                    )
                    
                    result['docbase_url'] = docbase_result['url']
                    result['docbase_id'] = docbase_result['id']
                    
                    print(f"✅ Docbaseアップロード完了")
                    print(f"📎 URL: {docbase_result['url']}")
                    
                except Exception as e:
                    print(f"❌ Docbaseアップロードエラー: {e}")
            
            return result
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _detect_category(self, product_name: str) -> str:
        """商品カテゴリの自動判定"""
        
        product_lower = product_name.lower()
        
        # アウトドア・キャンプ系
        if any(word in product_lower for word in 
               ['powerarq', 'camp', 'outdoor', 'portable', 'アウトドア', 'キャンプ']):
            return 'outdoor'
        
        # 電子機器・家電系
        elif any(word in product_lower for word in 
                 ['electric', 'electronic', 'blanket', '電気', '電子', '毛布', 'ブランケット']):
            return 'electronics'
        
        # ライフスタイル・インテリア系
        elif any(word in product_lower for word in 
                 ['lifestyle', 'interior', 'home', 'living', 'ライフスタイル', 'インテリア']):
            return 'lifestyle'
        
        else:
            return 'electronics'  # デフォルト
    
    def generate_comparison_report(self, analysis_result: Dict) -> str:
        """競合比較レポート生成"""
        
        if not analysis_result.get('competitor_analysis'):
            return "競合分析データがありません"
        
        competitor_analysis = analysis_result['competitor_analysis']
        product_name = analysis_result.get('product_name', '商品名不明')
        
        report = f"""# 競合分析レポート

## 📊 分析対象商品
**{product_name}**

## 🔍 市場分析サマリー
- **分析商品数**: {competitor_analysis.get('competitor_count', 0)}商品
- **分析日時**: {competitor_analysis.get('analysis_date', '不明')}
- **商品カテゴリ**: {analysis_result.get('category', '不明')}

## 💰 価格分析
"""
        
        best_practices = competitor_analysis.get('best_practices', {})
        price_range = best_practices.get('price_range', {})
        
        if price_range:
            report += f"""- **市場価格帯**: {price_range.get('min', 0):,}円 〜 {price_range.get('max', 0):,}円
- **平均価格**: {price_range.get('avg', 0):,}円
- **価格ポジション**: 自社商品の位置づけ分析が必要
"""
        
        # トップ訴求ポイント
        report += f"""
## 🎯 市場で成功している訴求ポイント
"""
        top_appeals = best_practices.get('top_appeals', [])
        for i, (appeal, count) in enumerate(top_appeals, 1):
            report += f"{i}. **{appeal}** (競合{count}社で使用)\n"
        
        # 効果的なページ構成
        report += f"""
## 📄 効果的なページ構成
"""
        effective_structures = best_practices.get('effective_structures', [])
        for i, (structure, count) in enumerate(effective_structures, 1):
            report += f"{i}. **{structure}** (競合{count}社で採用)\n"
        
        # 最適化提案
        optimized_appeals = competitor_analysis.get('optimized_appeals', [])
        if optimized_appeals:
            report += f"""
## ✨ 最適化された訴求ポイント（提案）
"""
            for i, appeal in enumerate(optimized_appeals, 1):
                report += f"{i}. {appeal}\n"
        
        # 改善提案
        recommendations = competitor_analysis.get('recommendations', {})
        if recommendations:
            report += f"""
## 🔧 改善提案

### ページ構成の改善
"""
            for rec in recommendations.get('page_structure', []):
                report += f"- {rec}\n"
            
            report += f"""
### コピー改善
"""
            for rec in recommendations.get('copy_improvements', []):
                report += f"- {rec}\n"
            
            report += f"""
### 機能強調ポイント
"""
            for feature in recommendations.get('feature_emphasis', []):
                report += f"- {feature}\n"
        
        report += f"""
## 📈 期待される効果
- **差別化の明確化**: 競合商品との違いを鮮明に
- **訴求力向上**: 市場で実証済みの成功パターン活用
- **コンバージョン改善**: 効果的なページ構成の採用

## 🎯 次のアクション
1. 提案された訴求ポイントの採用検討
2. ページ構成の最適化実行
3. 競合との差別化ポイント強化
4. 価格戦略の見直し検討
"""
        
        return report

def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("🚀 高度LPラフ案生成システム（競合分析機能付き）")
        print("\n使用方法:")
        print("  python advanced_lp_generator.py <規定書CSVファイル> [オプション]")
        print("\nオプション:")
        print("  --upload          Docbaseにアップロード")
        print("  --no-analysis     競合分析を無効化")
        print("  --report          競合分析レポートも生成")
        print("\n例:")
        print("  python advanced_lp_generator.py 規定書.csv")
        print("  python advanced_lp_generator.py 規定書.csv --upload")
        print("  python advanced_lp_generator.py 規定書.csv --upload --report")
        print("  python advanced_lp_generator.py 規定書.csv --no-analysis")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    upload_flag = '--upload' in sys.argv
    no_analysis_flag = '--no-analysis' in sys.argv
    report_flag = '--report' in sys.argv
    
    enable_analysis = not no_analysis_flag
    
    if not os.path.exists(csv_path):
        print(f"❌ 規定書CSVファイルが見つかりません: {csv_path}")
        sys.exit(1)
    
    try:
        # 高度LP生成実行
        generator = AdvancedLPGenerator()
        result = generator.generate_with_competitor_analysis(
            csv_path, 
            enable_analysis=enable_analysis, 
            upload_to_docbase=upload_flag
        )
        
        if not result:
            print("❌ 生成処理に失敗しました")
            sys.exit(1)
        
        # 競合分析レポート生成
        if report_flag and enable_analysis:
            try:
                print(f"\n📊 競合分析レポート生成中...")
                
                report_content = generator.generate_comparison_report(result)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                product_name = result.get('product_name', '商品名').replace(' ', '_')
                report_path = os.path.join('output', f'competitor_report_{product_name}_{timestamp}.md')
                
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                
                print(f"📊 競合分析レポート保存: {report_path}")
                result['report_path'] = report_path
                
            except Exception as e:
                print(f"⚠️ レポート生成エラー: {e}")
        
        # 結果サマリー表示
        print(f"\n🎉 生成完了！")
        print(f"📦 生成タイプ: {result.get('generation_type', '不明')}")
        print(f"📁 LPラフ案: {result.get('lp_output_path')}")
        
        if enable_analysis:
            competitor_count = result.get('competitor_analysis', {}).get('competitor_count', 0)
            print(f"🔍 競合分析: {competitor_count}商品を分析")
            if 'analysis_output_path' in result:
                print(f"📊 分析データ: {result['analysis_output_path']}")
        
        if report_flag and 'report_path' in result:
            print(f"📋 分析レポート: {result['report_path']}")
        
        if 'docbase_url' in result:
            print(f"🌐 Docbase URL: {result['docbase_url']}")
        
        print(f"\n✨ 高度LP生成システム完了")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()