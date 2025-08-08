#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マスターLPラフ案生成システム（全機能統合版）
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

# 既存モジュールをインポート
from enhanced_lp_generator import EnhancedLPGenerator
from layout_generator import LayoutGenerator
from docbase_lp_uploader import DocbaseLPUploader
from kishima_spec_to_lp import KishimaSpecToLPGenerator

class MasterLPGenerator:
    def __init__(self):
        """全機能を統合したマスタージェネレーターを初期化"""
        self.enhanced_generator = EnhancedLPGenerator()
        self.layout_generator = LayoutGenerator()
        self.docbase_uploader = DocbaseLPUploader()
        self.kishima_generator = KishimaSpecToLPGenerator()
    
    def generate_complete_lp_package(self, input_file: str, input_type: str = 'auto', 
                                   upload_to_docbase: bool = False) -> Dict[str, Any]:
        """完全なLPパッケージ（ラフ案+レイアウト指示書）を生成"""
        
        print(f"\n🚀 マスターLP生成システム開始")
        print(f"📁 入力ファイル: {input_file}")
        print(f"📊 入力タイプ: {input_type}")
        
        # 入力タイプの自動判定
        if input_type == 'auto':
            input_type = self._detect_input_type(input_file)
            print(f"🔍 自動判定結果: {input_type}")
        
        # 商品データ抽出
        try:
            product_data = self._extract_product_data(input_file, input_type)
            print(f"✅ 商品データ抽出完了: {product_data.get('product_name', '商品名不明')}")
        except Exception as e:
            print(f"❌ 商品データ抽出エラー: {e}")
            return None
        
        # 強化版LPラフ案生成
        try:
            enhanced_lp_content = self.enhanced_generator.generate_enhanced_lp_rough(product_data)
            print("✅ 強化版LPラフ案生成完了")
        except Exception as e:
            print(f"❌ LPラフ案生成エラー: {e}")
            return None
        
        # ページデータ抽出（レイアウト生成用）
        page_details = product_data.get('page_details', [])
        category = self.enhanced_generator.analyze_product_category(product_data)
        
        # レイアウト指示書生成
        try:
            layout_document = self.layout_generator.generate_layout_document(page_details, category)
            print("✅ レイアウト指示書生成完了")
        except Exception as e:
            print(f"❌ レイアウト指示書生成エラー: {e}")
            layout_document = "レイアウト指示書生成に失敗しました"
        
        # ファイル出力
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        product_name = product_data.get('product_name', '商品名').replace(' ', '_').replace('/', '_')
        
        # 出力ファイルパス
        lp_output_path = os.path.join('output', f'lp_rough_complete_{product_name}_{timestamp}.md')
        layout_output_path = os.path.join('output', f'layout_instructions_{product_name}_{timestamp}.md')
        data_output_path = os.path.join('output', f'product_data_{product_name}_{timestamp}.json')
        
        # ディレクトリ作成
        os.makedirs('output', exist_ok=True)
        
        # ファイル書き込み
        with open(lp_output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_lp_content)
        
        with open(layout_output_path, 'w', encoding='utf-8') as f:
            f.write(layout_document)
        
        with open(data_output_path, 'w', encoding='utf-8') as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 LPラフ案: {lp_output_path}")
        print(f"📁 レイアウト指示書: {layout_output_path}")
        print(f"📁 商品データ: {data_output_path}")
        
        result = {
            'lp_content': enhanced_lp_content,
            'layout_instructions': layout_document,
            'product_data': product_data,
            'output_files': {
                'lp_rough': lp_output_path,
                'layout_instructions': layout_output_path,
                'product_data': data_output_path
            },
            'category': category
        }
        
        # Docbaseアップロード
        if upload_to_docbase:
            try:
                print(f"\n📤 Docbaseアップロード開始...")
                
                # LPラフ案をアップロード
                lp_title = f"【LPラフ案・完全版】{product_data.get('product_name', '商品名')}"
                lp_tags = ['LPラフ案', 'マスター生成', 'レイアウト指示付き', category]
                
                # 商品カテゴリに応じたタグ追加
                if 'PowerArQ' in product_data.get('product_name', ''):
                    lp_tags.append('PowerArQ')
                
                lp_result = self.docbase_uploader.create_lp_post(lp_title, enhanced_lp_content, lp_tags)
                
                # レイアウト指示書をアップロード
                layout_title = f"【レイアウト指示書】{product_data.get('product_name', '商品名')}"
                layout_tags = ['レイアウト指示', 'デザイン制作', 'LP制作', category]
                
                layout_result = self.docbase_uploader.create_lp_post(layout_title, layout_document, layout_tags)
                
                result['docbase_results'] = {
                    'lp_rough': {
                        'url': lp_result['url'],
                        'id': lp_result['id']
                    },
                    'layout_instructions': {
                        'url': layout_result['url'],
                        'id': layout_result['id']
                    }
                }
                
                print(f"✅ Docbaseアップロード完了")
                print(f"📎 LPラフ案: {lp_result['url']}")
                print(f"📎 レイアウト指示書: {layout_result['url']}")
                
            except Exception as e:
                print(f"❌ Docbaseアップロードエラー: {e}")
        
        return result
    
    def _detect_input_type(self, file_path: str) -> str:
        """入力ファイルタイプを自動判定"""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.csv':
            # CSVファイル内容を確認してサブタイプ判定
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '規定書' in content or '加島商事' in content:
                        return 'kishima_csv'
                    else:
                        return 'csv'
            except:
                return 'csv'
        elif ext in ['.xlsx', '.xls']:
            return 'excel'
        elif ext == '.pdf':
            return 'pdf'
        elif ext == '.json':
            return 'json'
        else:
            return 'unknown'
    
    def _extract_product_data(self, file_path: str, input_type: str) -> Dict[str, Any]:
        """入力タイプに応じて商品データを抽出"""
        
        if input_type == 'kishima_csv':
            return self.kishima_generator.parse_kishima_csv(file_path)
        elif input_type == 'csv':
            # 通常のCSV処理（既存のcsv_to_json_simple.pyを使用）
            from csv_to_json_simple import parse_csv_to_json
            return parse_csv_to_json(file_path)
        elif input_type == 'excel':
            # Excel処理
            from excel_to_lp_generator import ExcelToLPGenerator
            excel_gen = ExcelToLPGenerator()
            return excel_gen.parse_excel_to_json(file_path)
        elif input_type == 'json':
            # JSON直接読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"未対応のファイルタイプ: {input_type}")
    
    def generate_image_checklist(self, product_data: Dict) -> str:
        """画像制作チェックリストを生成"""
        
        page_details = product_data.get('page_details', [])
        product_name = product_data.get('product_name', '商品名')
        
        checklist = f"""# 📸 画像制作チェックリスト
商品名: {product_name}
作成日: {datetime.now().strftime('%Y年%m月%d日')}

## 🎯 必要画像一覧

### 最優先画像（high priority）
"""
        
        high_priority_images = []
        medium_priority_images = []
        low_priority_images = []
        
        for i, page in enumerate(page_details, 1):
            priority = page.get('design_priority', 'medium')
            if page.get('has_images', False):
                image_info = {
                    'page': i,
                    'instruction': page.get('image_instruction', '画像準備中'),
                    'note': page.get('layout_note', '')
                }
                
                if priority == 'high':
                    high_priority_images.append(image_info)
                elif priority == 'medium':
                    medium_priority_images.append(image_info)
                else:
                    low_priority_images.append(image_info)
        
        # 優先度別にリスト化
        for img in high_priority_images:
            checklist += f"- [ ] **{img['page']}枚目**: {img['instruction']}\\n"
        
        checklist += "\\n### 重要画像（medium priority）\\n"
        for img in medium_priority_images:
            checklist += f"- [ ] **{img['page']}枚目**: {img['instruction']}\\n"
        
        if low_priority_images:
            checklist += "\\n### 補助画像（low priority）\\n"
            for img in low_priority_images:
                checklist += f"- [ ] **{img['page']}枚目**: {img['instruction']}\\n"
        
        # 制作仕様
        checklist += f"""

## 📏 制作仕様
- **PC版**: 1200px基準
- **SP版**: 850px基準  
- **解像度**: 72ppi（Web用）
- **フォーマット**: JPG（写真）、PNG（ロゴ・図表）
- **品質**: 高品質（ファイルサイズ最適化）

## ✅ 品質チェックポイント
- [ ] 商品が鮮明に写っている
- [ ] 背景が適切（白背景 or 自然な環境）
- [ ] ライティングが適切
- [ ] 商品の魅力が伝わる角度
- [ ] ブランドトーンに合致
- [ ] テキスト挿入スペースを確保
- [ ] レスポンシブ対応を考慮

## 📋 撮影・制作スケジュール
- [ ] 商品手配・準備
- [ ] 撮影日程調整
- [ ] スタジオ・機材準備
- [ ] 撮影実行
- [ ] 画像編集・加工
- [ ] レビュー・修正
- [ ] 最終納品

## 📞 制作体制
- **撮影**: 
- **編集**: 
- **確認**: 
- **最終承認**: 
"""
        
        return checklist

def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("🚀 マスターLPラフ案生成システム")
        print("\n使用方法:")
        print("  python master_generator.py <入力ファイル> [オプション]")
        print("\nオプション:")
        print("  --upload          Docbaseにアップロード")
        print("  --type <type>     入力タイプを指定 (auto|csv|excel|kishima_csv|json)")
        print("  --checklist       画像チェックリストも生成")
        print("\n例:")
        print("  python master_generator.py data/規定書.csv")
        print("  python master_generator.py templates/product.xlsx --upload")
        print("  python master_generator.py data/product.json --type json --upload --checklist")
        sys.exit(1)
    
    input_file = sys.argv[1]
    upload_flag = '--upload' in sys.argv
    checklist_flag = '--checklist' in sys.argv
    
    # タイプ指定の確認
    input_type = 'auto'
    if '--type' in sys.argv:
        type_index = sys.argv.index('--type')
        if type_index + 1 < len(sys.argv):
            input_type = sys.argv[type_index + 1]
    
    if not os.path.exists(input_file):
        print(f"❌ 入力ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    try:
        # マスター生成実行
        generator = MasterLPGenerator()
        result = generator.generate_complete_lp_package(
            input_file, 
            input_type=input_type, 
            upload_to_docbase=upload_flag
        )
        
        if not result:
            print("❌ 生成処理に失敗しました")
            sys.exit(1)
        
        # 画像チェックリスト生成
        if checklist_flag:
            try:
                checklist = generator.generate_image_checklist(result['product_data'])
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                product_name = result['product_data'].get('product_name', '商品名').replace(' ', '_')
                checklist_path = os.path.join('output', f'image_checklist_{product_name}_{timestamp}.md')
                
                with open(checklist_path, 'w', encoding='utf-8') as f:
                    f.write(checklist)
                
                print(f"📋 画像チェックリスト: {checklist_path}")
                result['output_files']['image_checklist'] = checklist_path
                
            except Exception as e:
                print(f"⚠️ 画像チェックリスト生成エラー: {e}")
        
        # 結果サマリー表示
        print(f"\n🎉 マスターLP生成完了！")
        print(f"📦 生成アイテム:")
        print(f"  ✅ LPラフ案（強化版）")
        print(f"  ✅ レイアウト指示書")
        print(f"  ✅ 商品データ（JSON）")
        if checklist_flag:
            print(f"  ✅ 画像制作チェックリスト")
        
        print(f"\n📁 出力ファイル:")
        for file_type, file_path in result['output_files'].items():
            print(f"  📄 {file_type}: {file_path}")
        
        if 'docbase_results' in result:
            print(f"\n🌐 Docbase URL:")
            for doc_type, doc_info in result['docbase_results'].items():
                print(f"  🔗 {doc_type}: {doc_info['url']}")
        
        print(f"\n🏷️ 商品カテゴリ: {result['category']}")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()