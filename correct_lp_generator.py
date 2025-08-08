#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正しいフォーマットでのLPラフ案生成システム
"""

import os
import sys
import csv
from datetime import datetime
from typing import Dict, Any, List
from docbase_lp_uploader import DocbaseLPUploader

class CorrectLPGenerator:
    def __init__(self):
        """初期化"""
        self.docbase_uploader = DocbaseLPUploader()
    
    def parse_kishima_csv(self, csv_path: str) -> Dict[str, Any]:
        """加島商事規定書CSVを正確に解析"""
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # データ抽出
        product_data = {}
        jan_codes = []
        
        for i, row in enumerate(rows):
            if len(row) >= 6 and row[4] and row[5]:
                key = row[4].strip()
                value = row[5].strip()
                product_data[key] = value
                
                # JANコード行の特別処理
                if "JANコード" in key:
                    # この行と次の行でJANコード情報を収集
                    jan_codes.append(value)
                    # 次の行もチェック
                    if i + 1 < len(rows) and len(rows[i + 1]) >= 6 and rows[i + 1][5]:
                        next_jan = rows[i + 1][5].strip()
                        if next_jan and ('：' in next_jan or ':' in next_jan):
                            jan_codes.append(next_jan)
        
        # JANコード情報をまとめる
        if jan_codes:
            product_data["JANコード\n（バリエーション別）"] = "\n".join(jan_codes)
        
        # セールスポイントの特別処理
        sales_points = []
        for i, row in enumerate(rows):
            if len(row) > 3 and row[3] and "セールスポイント" in row[3]:
                # セールスポイント行以降を取得
                for j in range(i+1, len(rows)):
                    if len(rows[j]) > 3 and rows[j][3]:
                        point_text = rows[j][3].strip()
                        if point_text.startswith("●"):
                            sales_points.append(point_text.replace("●", "").strip())
                break
        
        product_data["セールスポイント"] = sales_points
        
        return product_data
    
    def generate_correct_lp_rough(self, product_data: Dict) -> str:
        """正しいフォーマットのLPラフ案を生成"""
        
        # 基本情報取得
        product_name = product_data.get('商品名', 'PowerArQ Electric Blanket Lite')
        product_kana = product_data.get('商品名カナ', '')
        model_number = product_data.get('メーカー型番', '')
        jan_info = product_data.get('JANコード\n（バリエーション別）', '')
        size = product_data.get('商品サイズ(cm)', '')
        weight = product_data.get('1個 重量(kg)', '')
        power = product_data.get('定格', '')
        material = product_data.get('表面素材', '')
        release_date = product_data.get('発売日', '')
        sales_points = product_data.get('セールスポイント', [])
        
        # JANコードの解析（複数行対応）
        jan_colors = []
        if jan_info:
            # まず全体のテキストから色とJANを抽出
            full_text = jan_info.replace('\n', ' ')
            # ブラックとベージュの情報を個別に処理
            # 正規表現的な処理でより確実に抽出
            import re
            color_patterns = [
                (r'ブラック[：:]\s*(\d+)', 'ブラック'),
                (r'ベージュ[：:]\s*(\d+)', 'ベージュ')
            ]
            
            for pattern, color in color_patterns:
                match = re.search(pattern, full_text)
                if match:
                    jan_colors.append({'color': color, 'jan': match.group(1)})
        
        # LPラフ案生成
        lp_content = f"""# LPラフ
## 作成の目的、意図
{product_name}の販売促進とブランド認知向上のため

## 対象商品
### 商品名
{product_name}
{f"（{product_kana}）" if product_kana else ""}

### SKU・JAN
| 種類 | SKU | JAN |
| --- | --- | --- |
"""
        
        # SKU・JANテーブル
        if jan_colors:
            for item in jan_colors:
                sku = f"{model_number}-{item['color']}" if model_number else f"PAQ-{item['color']}"
                lp_content += f"| {item['color']} | {sku} | {item['jan']} |\n"
        else:
            lp_content += "| カラー・サイズ | SKUコード | JANコード |\n"
        
        # 基本情報
        lp_content += f"""
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

下記、トンマナを踏まえて作成お願いします。
（別途共有）

### ベースのデータ

（別途共有）

---
# LP構成
| 枚数 | コンテンツ概要 |
| --- | --- |
| 1枚目 | TOPキャッチ |
| 2枚目 | 売れている訴求・実績 |
| 3枚目 | ブランド価値・安全性 |
| 4枚目 | メイン機能・特徴1（10段階温度調節） |
| 5枚目 | メイン機能・特徴2（過熱保護・安全性） |
| 6枚目 | 使用シーン |
| 7枚目 | サイズ・スペック詳細 |
| 8枚目 | 付属品・同梱物 |
| 9枚目 | 保証・アフターサービス |
| 10枚目 | よくある質問 |

---
# ラフ詳細

## 1枚目

### レイアウト案
【画像準備中】

商品の魅力が一目で伝わるデザインにしてください。

### テキスト

{product_name}

{f"キャンプギアに合うデザイン" if sales_points and any("キャンプ" in point for point in sales_points) else "快適な温もりを"}

{f"• 10段階の温度調節" if sales_points and any("10段階" in point for point in sales_points) else ""}
{f"• 過熱保護システム搭載" if sales_points and any("過熱保護" in point for point in sales_points) else ""}
{f"• 丸洗い可能" if sales_points and any("丸洗い" in point for point in sales_points) else ""}

### 使用画像

【画像準備中】

## 2枚目

### レイアウト案
【画像準備中】

数字やロゴを効果的に配置してください。

### テキスト

PowerARQブランド

信頼の実績
累計販売台数○○万台突破
※2025年○月時点

## 3枚目

### レイアウト案
【画像準備中】

### テキスト

PowerARQブランドの安心品質

日本ブランドとしての品質・安全性

### 使用画像

【画像準備中】

## 4枚目

### レイアウト案
【画像準備中】

### テキスト

10段階の温度調節

お好みの温かさに細かく設定
{f"コントローラーから簡単操作" if sales_points and any("コントローラー" in point for point in sales_points) else ""}

### 使用画像

【画像準備中】

## 5枚目

### レイアウト案
【画像準備中】

### テキスト

安全機能搭載

{f"過熱保護システム" if sales_points and any("過熱保護" in point for point in sales_points) else "安全機能"}
安心してお使いいただけます

### 使用画像

【画像準備中】

## 6枚目

### レイアウト案
【画像準備中】

### テキスト

いつでも、どこでも暖かく

{f"キャンプ・アウトドア・自宅" if sales_points and any("キャンプ" in point for point in sales_points) else "リビング・寝室・書斎"}
あらゆるシーンで活躍

### 使用画像

【画像準備中】

## 7枚目

### レイアウト案
【画像準備中】

### テキスト

仕様・スペック

{f"サイズ：{size}" if size else ""}
{f"重量：{weight}" if weight else ""}
{f"定格：{power}" if power else ""}
{f"素材：{material}" if material else ""}

### 使用画像

【画像準備中】

## 8枚目

### レイアウト案
【画像準備中】

### テキスト

付属品・同梱物

コントローラー
取扱説明書
保証書

### 使用画像

【画像準備中】

## 9枚目

### レイアウト案
【画像準備中】

### テキスト

安心の保証・アフターサービス

メーカー保証
充実のサポート体制

## 10枚目

### レイアウト案
【画像準備中】

### テキスト

よくある質問

Q: 電気代はどのくらいかかりますか？
A: 1時間あたり約○円です（中間設定時）

{f"Q: 丸洗いできますか？" if sales_points and any("丸洗い" in point for point in sales_points) else "Q: お手入れ方法は？"}
{f"A: はい、丸洗い可能です" if sales_points and any("丸洗い" in point for point in sales_points) else "A: 簡単なお手入れで清潔に保てます"}

"""
        
        return lp_content
    
    def generate_from_kishima_csv(self, csv_path: str, upload_to_docbase: bool = False) -> Dict[str, Any]:
        """加島商事規定書CSVから正しいLPラフ案を生成"""
        
        print(f"\n📋 規定書解析開始: {csv_path}")
        
        try:
            # データ抽出
            product_data = self.parse_kishima_csv(csv_path)
            print(f"✅ 規定書解析完了: {product_data.get('商品名', '商品名不明')}")
            
            # LPラフ案生成
            lp_content = self.generate_correct_lp_rough(product_data)
            print("✅ LPラフ案生成完了")
            
            # ファイル保存
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            product_name = product_data.get('商品名', '商品名').replace(' ', '_')
            output_filename = f"lp_rough_correct_{product_name}_{timestamp}.md"
            output_path = os.path.join('output', output_filename)
            
            os.makedirs('output', exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(lp_content)
            
            print(f"📁 出力ファイル: {output_path}")
            
            result = {
                'lp_content': lp_content,
                'output_path': output_path,
                'product_data': product_data
            }
            
            # Docbaseアップロード
            if upload_to_docbase:
                try:
                    title = f"【LPラフ案】{product_data.get('商品名', '商品名')}"
                    tags = ['LPラフ案', '正式版', '規定書生成']
                    
                    if 'PowerArQ' in product_data.get('商品名', ''):
                        tags.extend(['PowerArQ', '電気毛布'])
                    
                    print(f"\n📤 Docbaseアップロード中...")
                    docbase_result = self.docbase_uploader.create_lp_post(title, lp_content, tags)
                    
                    result['docbase_url'] = docbase_result['url']
                    result['docbase_id'] = docbase_result['id']
                    
                    print(f"✅ Docbaseアップロード完了")
                    print(f"📎 URL: {docbase_result['url']}")
                    
                except Exception as e:
                    print(f"❌ Docbaseアップロードエラー: {e}")
            
            return result
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            return None

def main():
    """メイン処理"""
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python correct_lp_generator.py <規定書CSVファイル> [--upload]")
        print("\n例:")
        print("  python correct_lp_generator.py 規定書.csv")
        print("  python correct_lp_generator.py 規定書.csv --upload")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    upload_flag = '--upload' in sys.argv
    
    if not os.path.exists(csv_path):
        print(f"❌ 規定書CSVファイルが見つかりません: {csv_path}")
        sys.exit(1)
    
    try:
        generator = CorrectLPGenerator()
        result = generator.generate_from_kishima_csv(csv_path, upload_to_docbase=upload_flag)
        
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