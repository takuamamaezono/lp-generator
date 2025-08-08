#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加島商事の規定書CSVからLPラフ案を直接生成するスクリプト
"""

import os
import sys
import csv
import json
from datetime import datetime
from typing import Dict, Any, List
from lp_rough_generator import LPRoughGenerator
from docbase_lp_uploader import DocbaseLPUploader

class KishimaSpecToLPGenerator:
    def __init__(self):
        """初期化"""
        self.lp_generator = LPRoughGenerator()
        
    def parse_kishima_csv(self, csv_path: str) -> Dict[str, Any]:
        """加島商事規定書CSVを解析してLP用データに変換"""
        
        # CSVファイル読み込み
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # データ抽出用の辞書
        spec_data = {}
        
        for row in rows:
            if len(row) >= 6:
                if row[4]:  # キー（項目名）がある場合
                    key = row[4].strip()
                    value = row[5].strip() if row[5] else ""
                    
                    if key and value:
                        spec_data[key] = value
                
                # セールスポイントの特別処理
                if row[3] and row[3].strip() == "セールスポイント":
                    sales_points = []
                    for i in range(len(rows)):
                        if i > rows.index(row) and rows[i][3]:
                            point = rows[i][3].strip()
                            if point and point.startswith("●"):
                                sales_points.append(point.replace("●", "").strip())
                    spec_data["セールスポイント"] = "\\n".join(sales_points)
                    break
        
        # LPラフ案用のデータ構造に変換
        product_data = {
            'product_name': spec_data.get('商品名', 'PowerArQ Electric Blanket Lite'),
            'product_kana': spec_data.get('商品名カナ', ''),
            'model_number': spec_data.get('メーカー型番', ''),
            'purpose': 'PowerArQ Electric Blanket Liteの販売促進とブランド認知向上のため',
            'price': '調整中（メーカー希望小売価格）',
            'release_date': spec_data.get('発売日', '2025年9月30日'),
            'target_platform': 'EC・キャンプ用品店・家電量販店',
            'target_users': 'キャンパー、寒がりの方、電気代を節約したい方、アウトドア愛好家',
            'main_appeal': '10段階温度設定×アウトドア対応で快適な温もりを',
            'brand_value': 'PowerARQブランドの信頼性とアウトドア特化設計',
            'specifications': {
                'サイズ': spec_data.get('商品サイズ(cm)', '約188×130cm'),
                '重量': spec_data.get('1個 重量(kg)', '約2.0kg'),
                '定格': spec_data.get('定格', '交流100V / 115W'),
                '表面素材': spec_data.get('表面素材', 'ポリエステル：100%'),
                '表面温度': spec_data.get('表面温度', '約XX℃'),
                '温度調節': '10段階',
                '安全機能': '過熱保護システム',
                'メンテナンス': '丸洗い可能'
            },
            'design_variants': self._extract_jan_codes(spec_data.get('JANコード\n（バリエーション別）', '')),
            'sku_list': self._create_sku_list(spec_data.get('JANコード\n（バリエーション別）', ''), spec_data.get('メーカー型番', '')),
            'main_features': self._extract_sales_points(spec_data.get('セールスポイント', '')),
            'lp_structure': [
                'TOPキャッチ・商品紹介',
                'PowerARQブランド×アウトドア',
                '10段階温度調節機能',
                'アウトドア対応素材・デザイン',
                '使用シーン・キャンプライフ',
                'サイズ・スペック詳細',
                'カラーバリエーション',
                '安全機能・メンテナンス',
                'よくある質問',
                '購入特典・販売店情報'
            ],
            'page_details': self._create_page_details(spec_data)
        }
        
        return product_data
    
    def _extract_jan_codes(self, jan_text: str) -> List[str]:
        """JANコード文字列からカラーバリエーションを抽出"""
        if not jan_text:
            return ['ブラック', 'ベージュ']
        
        colors = []
        lines = jan_text.split('\n') if '\n' in jan_text else [jan_text]
        for line in lines:
            if '：' in line:
                color = line.split('：')[0].strip()
                if color:
                    colors.append(color)
        return colors if colors else ['ブラック', 'ベージュ']
    
    def _create_sku_list(self, jan_text: str, model_number: str) -> List[Dict]:
        """SKUリストを作成"""
        sku_list = []
        colors = self._extract_jan_codes(jan_text)
        jan_codes = self._extract_jan_numbers(jan_text)
        
        for i, color in enumerate(colors):
            jan_code = jan_codes[i] if i < len(jan_codes) else '4571427130640'
            sku_code = f"{model_number}-{color[:2].upper()}" if model_number else f"PAQ-BLANKET-{color[:2].upper()}"
            
            sku_list.append({
                'type': color,
                'sku': sku_code,
                'jan': jan_code
            })
        
        return sku_list
    
    def _extract_jan_numbers(self, jan_text: str) -> List[str]:
        """JANコード番号を抽出"""
        if not jan_text:
            return ['4571427130640', '4571427130657']
        
        jan_numbers = []
        lines = jan_text.split('\n') if '\n' in jan_text else [jan_text]
        for line in lines:
            if '：' in line:
                jan = line.split('：')[1].strip()
                if jan and jan.isdigit():
                    jan_numbers.append(jan)
        return jan_numbers if jan_numbers else ['4571427130640', '4571427130657']
    
    def _extract_sales_points(self, sales_text: str) -> List[str]:
        """セールスポイントを特徴リストに変換"""
        if not sales_text:
            return [
                '10段階の温度調節機能',
                'アウトドア向けデザイン',
                '過熱保護システム搭載',
                '丸洗い可能',
                'PowerARQブランド'
            ]
        
        features = []
        points = sales_text.split('\\n')
        for point in points:
            if point.strip():
                # セールスポイントを特徴に変換
                if '温度設定' in point:
                    features.append('10段階の温度調節機能')
                elif 'カラーデザイン' in point or 'インテリア' in point:
                    features.append('キャンプギアに合うデザイン')
                elif '電熱線' in point or '暖か' in point:
                    features.append('より暖かさを感じやすい素材感')
                elif '過熱保護' in point:
                    features.append('過熱保護システム搭載')
                elif '丸洗い' in point:
                    features.append('丸洗い可能でメンテナンス簡単')
        
        return features if features else [
            '10段階の温度調節機能',
            'アウトドア向けデザイン', 
            '過熱保護システム搭載',
            '丸洗い可能'
        ]
    
    def _create_page_details(self, spec_data: Dict) -> List[Dict]:
        """ページ詳細データを作成"""
        product_name = spec_data.get('商品名', 'PowerArQ Electric Blanket Lite')
        
        page_details = [
            {
                'text': f'{product_name}\\n\\nアウトドアでも暖かく\\n\\n• 10段階の温度調節\\n• キャンプギアに合うデザイン\\n• 丸洗い可能',
                'layout_note': 'アウトドアシーンでの商品使用イメージ',
                'has_images': True
            },
            {
                'text': 'PowerARQブランド×アウトドア\\n\\n信頼のブランドが提案する\\n新しいアウトドア体験',
                'layout_note': 'ブランドロゴとアウトドアシーン',
                'has_images': True
            },
            {
                'text': '10段階の温度調節\\n\\nコントローラーで簡単操作\\n\\n体調や気候に合わせて\\nお好みの暖かさに',
                'layout_note': 'コントローラーの操作イメージ',
                'has_images': True
            },
            {
                'text': 'アウトドア対応素材\\n\\nより暖かさを感じやすい\\n電熱線配置とポリエステル素材',
                'layout_note': '素材の質感と電熱線配置の説明',
                'has_images': True
            },
            {
                'text': 'キャンプから自宅まで\\n\\nテント内・車中泊・リビング\\nあらゆるシーンで活躍',
                'layout_note': '様々な使用シーンの写真',
                'has_images': True
            },
            {
                'text': f'仕様・スペック\\n\\n{spec_data.get("商品サイズ(cm)", "約188×130cm")}\\n{spec_data.get("1個 重量(kg)", "約2.0kg")}\\n{spec_data.get("定格", "交流100V / 115W")}',
                'layout_note': 'スペック表とサイズ感の比較',
                'has_images': True
            },
            {
                'text': 'カラーバリエーション\\n\\nブラック・ベージュの2色展開\\nキャンプギアに合わせてお選びください',
                'layout_note': '2色並べたカラー比較',
                'has_images': True
            },
            {
                'text': '安全機能・メンテナンス\\n\\n過熱保護システム搭載\\n丸洗い可能で清潔に使用',
                'layout_note': '安全機能と洗濯方法の説明',
                'has_images': True
            },
            {
                'text': 'よくある質問\\n\\nQ: キャンプで使えますか？\\nA: はい、AC電源があれば屋外でも使用可能です',
                'layout_note': 'FAQ形式で見やすく',
                'has_images': False
            },
            {
                'text': '販売店情報\\n\\n全国のアウトドア用品店\\n家電量販店で販売予定',
                'layout_note': '販売店ロゴと購入方法',
                'has_images': True
            }
        ]
        
        return page_details
    
    def generate_lp_from_kishima_csv(self, csv_path: str, upload_to_docbase: bool = False) -> Dict[str, Any]:
        """加島商事規定書CSVからLPラフ案を生成"""
        print(f"\n📋 規定書解析開始: {csv_path}")
        
        # CSV解析
        try:
            product_data = self.parse_kishima_csv(csv_path)
            print(f"✅ 規定書解析完了: {product_data['product_name']}")
        except Exception as e:
            print(f"❌ 規定書読み込みエラー: {e}")
            return None
        
        # LPラフ案生成
        lp_content = self.lp_generator.generate_lp_rough(product_data)
        
        # ファイル保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        product_name = product_data['product_name'].replace(' ', '_')
        output_filename = f"lp_rough_{product_name}_{timestamp}.md"
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
                tags = ['LPラフ案', 'PowerArQ', '電気毛布', '規定書生成', 'アウトドア']
                
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
        print("  python kishima_spec_to_lp.py <規定書CSVファイル> [--upload]")
        print("\n例:")
        print("  python kishima_spec_to_lp.py /path/to/規定書一覧_加島商事 - 電気毛布（廉価版）.csv")
        print("  python kishima_spec_to_lp.py /path/to/規定書一覧_加島商事 - 電気毛布（廉価版）.csv --upload")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    upload_flag = '--upload' in sys.argv
    
    if not os.path.exists(csv_path):
        print(f"❌ 規定書CSVファイルが見つかりません: {csv_path}")
        sys.exit(1)
    
    try:
        generator = KishimaSpecToLPGenerator()
        result = generator.generate_lp_from_kishima_csv(csv_path, upload_to_docbase=upload_flag)
        
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