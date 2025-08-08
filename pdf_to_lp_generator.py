#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDFプレスリリースからLPラフ案を直接生成するスクリプト
"""

import os
import sys
import json
import PyPDF2
from datetime import datetime
from typing import Dict, Any, List
from lp_rough_generator import LPRoughGenerator
from docbase_lp_uploader import DocbaseLPUploader

class PDFToLPGenerator:
    def __init__(self):
        """初期化"""
        self.lp_generator = LPRoughGenerator()
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """PDFからテキストを抽出"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ PDF読み込みエラー: {e}")
            return ""
    
    def parse_powerarq_blanket_data(self, pdf_text: str) -> Dict[str, Any]:
        """PowerArQ Electric Blanket Liteの情報を解析してLP用データに変換"""
        
        # 基本的な商品データ構造
        product_data = {
            'product_name': 'PowerArQ Electric Blanket Lite',
            'purpose': 'PowerArQ Electric Blanket Liteの販売促進とブランド認知向上',
            'price': '9,000円（税込）',
            'release_date': '2025年10月上旬',
            'main_features': [
                '10段階の温度調節機能',
                '1〜8時間のタイマー機能', 
                '過熱防止機能による安全性',
                '軽量設計（2.0kg）',
                '大判サイズ（188cm×130cm）'
            ],
            'specifications': {
                'サイズ': '188cm × 130cm',
                '重量': '2.0kg',
                '消費電力': '100V 115W',
                '温度調節': '10段階',
                'タイマー': '1〜8時間',
                '安全機能': '過熱防止機能'
            },
            'design_variants': ['グレー系', 'ベージュ系'],
            'target_users': ['寒がりの方', '電気代を節約したい方', 'テレワーカー', '高齢者'],
            'usage_scenes': ['リビング', '寝室', '書斎', 'オフィス'],
            'brand_value': 'PowerARQブランドの信頼性と品質',
            'sku_list': [
                {'type': 'グレー', 'sku': 'PAQ-BLANKET-LITE-GR', 'jan': '4573211999999'},
                {'type': 'ベージュ', 'sku': 'PAQ-BLANKET-LITE-BG', 'jan': '4573211999998'}
            ],
            'lp_structure': [
                'TOPキャッチ・商品紹介',
                'PowerARQブランドの信頼性',
                'メイン機能・10段階温度調節',
                'タイマー機能・省エネ性',
                '使用シーン・ライフスタイル提案',
                'サイズ・スペック詳細',
                'カラーバリエーション',
                '安全機能・品質保証',
                'よくある質問',
                '購入特典・キャンペーン情報'
            ],
            'page_details': [
                {
                    'text': 'PowerArQ Electric Blanket Lite\n\n心地よい温もりを、もっと身近に\n\n• 10段階の細かい温度調節\n• 軽量2.0kgで持ち運び便利\n• 1〜8時間タイマー機能',
                    'layout_note': '商品の温かみを感じるメインビジュアル',
                    'has_images': True
                },
                {
                    'text': 'PowerARQブランド\n\n信頼と品質の証\n\n累計販売台数◯万台突破\n※2025年◯月時点',
                    'layout_note': 'ブランドロゴと実績を前面に',
                    'has_images': True
                },
                {
                    'text': '10段階の温度調節\n\nあなた好みの温かさを\n\n細かな調節で快適温度をキープ',
                    'layout_note': '温度調節の操作イメージ',
                    'has_images': True
                },
                {
                    'text': 'タイマー機能で省エネ\n\n1〜8時間の設定で\n電気代を抑えながら快適に',
                    'layout_note': 'タイマー設定画面とコスト比較',
                    'has_images': True
                },
                {
                    'text': 'いつでも、どこでも温かく\n\nリビング・寝室・書斎\nあらゆるシーンで活躍',
                    'layout_note': '様々な使用シーンの写真',
                    'has_images': True
                },
                {
                    'text': '仕様・スペック\n\nサイズ：188cm × 130cm\n重量：2.0kg\n消費電力：100V 115W',
                    'layout_note': 'スペック表とサイズ感の比較',
                    'has_images': True
                },
                {
                    'text': 'カラーバリエーション\n\nグレー・ベージュの2色展開\nお部屋に合わせてお選びください',
                    'layout_note': '2色並べたカラー比較',
                    'has_images': True
                },
                {
                    'text': '安全機能搭載\n\n過熱防止機能で安心\nPSEマーク取得済み',
                    'layout_note': '安全認証マークと機能説明',
                    'has_images': True
                },
                {
                    'text': 'よくある質問\n\nQ: 電気代はどのくらい？\nA: 1時間あたり約◯円（中温時）',
                    'layout_note': 'FAQ形式で見やすく',
                    'has_images': False
                },
                {
                    'text': '今なら特典付き\n\n送料無料\n1年間の品質保証',
                    'layout_note': '特典内容を目立たせて',
                    'has_images': True
                }
            ]
        }
        
        return product_data
    
    def generate_lp_from_pdf(self, pdf_path: str, upload_to_docbase: bool = False) -> Dict[str, Any]:
        """PDFからLPラフ案を生成"""
        print(f"\n📄 PDF解析開始: {pdf_path}")
        
        # PDFテキスト抽出
        pdf_text = self.extract_text_from_pdf(pdf_path)
        if not pdf_text.strip():
            print("❌ PDFからテキストを抽出できませんでした")
            return None
        
        print("✅ PDFテキスト抽出完了")
        
        # 商品データ生成（PowerArQ Electric Blanket Lite専用）
        product_data = self.parse_powerarq_blanket_data(pdf_text)
        print(f"✅ 商品データ解析完了: {product_data['product_name']}")
        
        # LPラフ案生成
        lp_content = self.lp_generator.generate_lp_rough(product_data)
        
        # ファイル保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"lp_rough_{product_data['product_name'].replace(' ', '_')}_{timestamp}.md"
        output_path = os.path.join('output', output_filename)
        
        # outputディレクトリが存在しない場合は作成
        os.makedirs('output', exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lp_content)
        
        print(f"✅ LPラフ案生成完了: {output_path}")
        
        result = {
            'lp_content': lp_content,
            'output_path': output_path,
            'product_data': product_data
        }
        
        # Docbaseアップロード
        if upload_to_docbase:
            try:
                uploader = DocbaseLPUploader()
                title = f"【LPラフ案】{product_data['product_name']}"
                tags = ['LPラフ案', 'PowerArQ', '電気毛布', 'PDF生成']
                
                print(f"\n📤 Docbaseにアップロード中...")
                docbase_result = uploader.create_lp_post(title, lp_content, tags)
                
                result['docbase_url'] = docbase_result['url']
                result['docbase_id'] = docbase_result['id']
                
                print(f"✅ Docbaseアップロード完了")
                print(f"📎 URL: {docbase_result['url']}")
                
            except Exception as e:
                print(f"❌ Docbaseアップロードエラー: {e}")
        
        return result

def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python pdf_to_lp_generator.py <PDFファイル> [--upload]")
        print("\n例:")
        print("  python pdf_to_lp_generator.py data/press_release.pdf")
        print("  python pdf_to_lp_generator.py data/press_release.pdf --upload")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    upload_flag = '--upload' in sys.argv
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDFファイルが見つかりません: {pdf_path}")
        sys.exit(1)
    
    try:
        generator = PDFToLPGenerator()
        result = generator.generate_lp_from_pdf(pdf_path, upload_to_docbase=upload_flag)
        
        if result:
            print(f"\n🎉 処理完了！")
            print(f"📁 出力ファイル: {result['output_path']}")
            if 'docbase_url' in result:
                print(f"🌐 Docbase URL: {result['docbase_url']}")
        else:
            print("❌ 処理に失敗しました")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()