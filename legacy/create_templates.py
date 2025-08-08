#!/usr/bin/env python3
"""
LP欄テンプレート作成スクリプト
各業界・商品タイプ別のテンプレートを作成します
"""

import json
import os


def create_template_dir():
    """テンプレートディレクトリを作成"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    return template_dir


def save_template(template_dir, name, data):
    """テンプレートを保存"""
    path = os.path.join(template_dir, f"{name}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ テンプレート作成: {name}")


def main():
    """各種テンプレートを作成"""
    template_dir = create_template_dir()
    
    # 1. 電子機器・ガジェット向けテンプレート
    electronics_template = {
        "product_name": "【商品名】",
        "catch_copy": "【例：最新テクノロジーで、あなたの生活をもっと便利に】",
        "price": "【価格】",
        "tax_included": True,
        "category": "電子機器",
        "features": [
            {
                "title": "高性能プロセッサ",
                "description": "最新のチップセットを搭載し、サクサクな動作を実現"
            },
            {
                "title": "長時間バッテリー",
                "description": "一日中使える大容量バッテリーを搭載"
            },
            {
                "title": "スタイリッシュなデザイン",
                "description": "洗練されたデザインで、どんなシーンにもマッチ"
            }
        ],
        "target_customer": "テクノロジーに興味がある方、効率的な作業環境を求める方",
        "solve_problems": [
            "処理速度が遅くてストレスを感じる",
            "バッテリーがすぐに切れて困る",
            "デザインが古臭い"
        ],
        "main_image": "【メイン画像URL】",
        "sub_images": ["【詳細画像URL1】", "【詳細画像URL2】"],
        "use_scenes": [
            "オフィスでの業務効率化",
            "カフェでのリモートワーク",
            "プレゼンテーション"
        ],
        "purchase_link": "【購入ページURL】",
        "contact_info": "お電話: 【電話番号】\nメール: 【メールアドレス】"
    }
    save_template(template_dir, "electronics_template", electronics_template)
    
    # 2. アウトドア・キャンプ用品テンプレート
    outdoor_template = {
        "product_name": "【商品名】",
        "catch_copy": "【例：大自然を、もっと身近に。快適なアウトドアライフを】",
        "price": "【価格】",
        "tax_included": True,
        "category": "アウトドア用品",
        "features": [
            {
                "title": "防水・防塵性能",
                "description": "IP65準拠で、雨や砂埃から守ります"
            },
            {
                "title": "コンパクト設計",
                "description": "持ち運びやすい軽量・コンパクトボディ"
            },
            {
                "title": "多機能性",
                "description": "1台で複数の用途に対応できる万能アイテム"
            }
        ],
        "target_customer": "キャンプ・登山を楽しむ方、災害時の備えをしたい方、車中泊をされる方",
        "solve_problems": [
            "荷物が多くて持ち運びが大変",
            "悪天候時の対応に困る",
            "電源確保が難しい"
        ],
        "main_image": "【メイン画像URL】",
        "sub_images": ["【使用シーン画像URL】", "【サイズ比較画像URL】"],
        "use_scenes": [
            "キャンプ場での使用",
            "登山・トレッキング",
            "災害時の備え",
            "車中泊"
        ],
        "purchase_link": "【購入ページURL】",
        "contact_info": "お電話: 【電話番号】\nメール: 【メールアドレス】",
        "notes": "※使用環境により性能が異なる場合があります"
    }
    save_template(template_dir, "outdoor_template", outdoor_template)
    
    # 3. 美容・健康商品テンプレート
    beauty_health_template = {
        "product_name": "【商品名】",
        "catch_copy": "【例：内側から輝く、本来の美しさを引き出す】",
        "price": "【価格】",
        "tax_included": True,
        "category": "美容・健康",
        "features": [
            {
                "title": "天然由来成分",
                "description": "肌に優しい自然由来の成分を厳選使用"
            },
            {
                "title": "臨床試験済み",
                "description": "効果と安全性を確認済み"
            },
            {
                "title": "簡単ケア",
                "description": "毎日続けやすいシンプルなケア方法"
            }
        ],
        "target_customer": "美容に関心の高い方、エイジングケアをしたい方、自然派コスメを好む方",
        "solve_problems": [
            "肌の乾燥やハリ不足",
            "年齢による肌の変化",
            "化学成分による肌トラブル"
        ],
        "main_image": "【商品イメージ画像URL】",
        "sub_images": ["【使用前後の比較画像URL】", "【成分説明画像URL】"],
        "use_scenes": [
            "朝晩のスキンケアルーティン",
            "特別な日の前のスペシャルケア",
            "旅行先でのケア"
        ],
        "purchase_link": "【購入ページURL】",
        "contact_info": "お電話: 【電話番号】\nメール: 【メールアドレス】",
        "notes": "※効果には個人差があります\n※アレルギーをお持ちの方は成分表をご確認ください"
    }
    save_template(template_dir, "beauty_health_template", beauty_health_template)
    
    # 4. 食品・飲料テンプレート
    food_beverage_template = {
        "product_name": "【商品名】",
        "catch_copy": "【例：毎日の食卓に、特別なひとときを】",
        "price": "【価格】",
        "tax_included": True,
        "category": "食品・飲料",
        "features": [
            {
                "title": "厳選素材",
                "description": "産地にこだわった上質な素材を使用"
            },
            {
                "title": "無添加・保存料不使用",
                "description": "体に優しい自然な味わい"
            },
            {
                "title": "便利な個包装",
                "description": "いつでも新鮮な状態でお楽しみいただけます"
            }
        ],
        "target_customer": "健康志向の方、本物の味を求める方、贈り物を探している方",
        "solve_problems": [
            "添加物が気になる",
            "美味しくて健康的な食品を探している",
            "贈り物に最適な商品を探している"
        ],
        "main_image": "【商品画像URL】",
        "sub_images": ["【調理例画像URL】", "【パッケージ画像URL】"],
        "use_scenes": [
            "毎日の食事",
            "特別な日のディナー",
            "ギフト・贈答品",
            "パーティーや集まり"
        ],
        "purchase_link": "【購入ページURL】",
        "contact_info": "お電話: 【電話番号】\nメール: 【メールアドレス】",
        "notes": "賞味期限：製造日より【期間】\n保存方法：【保存方法】\nアレルギー表示：【アレルギー情報】"
    }
    save_template(template_dir, "food_beverage_template", food_beverage_template)
    
    # 5. ファッション・アパレルテンプレート
    fashion_template = {
        "product_name": "【商品名】",
        "catch_copy": "【例：あなたらしさを表現する、こだわりの一着】",
        "price": "【価格】",
        "tax_included": True,
        "category": "ファッション",
        "features": [
            {
                "title": "高品質素材",
                "description": "肌触りが良く、長く愛用できる素材を使用"
            },
            {
                "title": "日本製",
                "description": "熟練の職人による丁寧な仕上がり"
            },
            {
                "title": "豊富なサイズ展開",
                "description": "XS〜3XLまで幅広いサイズをご用意"
            }
        ],
        "target_customer": "質の良い服を長く着たい方、シンプルで上品なスタイルを好む方",
        "solve_problems": [
            "サイズが合う服が見つからない",
            "すぐに型崩れしてしまう",
            "着心地の良い服が欲しい"
        ],
        "main_image": "【着用イメージ画像URL】",
        "sub_images": ["【素材アップ画像URL】", "【カラーバリエーション画像URL】"],
        "use_scenes": [
            "オフィスカジュアル",
            "週末のお出かけ",
            "フォーマルな場面"
        ],
        "purchase_link": "【購入ページURL】",
        "contact_info": "お電話: 【電話番号】\nメール: 【メールアドレス】",
        "notes": "サイズ表：【サイズ表へのリンク】\nお手入れ方法：【洗濯表示】"
    }
    save_template(template_dir, "fashion_template", fashion_template)
    
    print("\n✨ すべてのテンプレートを作成しました！")
    print(f"保存場所: {template_dir}")
    print("\n利用可能なテンプレート:")
    print("- electronics_template: 電子機器・ガジェット向け")
    print("- outdoor_template: アウトドア・キャンプ用品向け")
    print("- beauty_health_template: 美容・健康商品向け")
    print("- food_beverage_template: 食品・飲料向け")
    print("- fashion_template: ファッション・アパレル向け")


if __name__ == "__main__":
    main()