# 🚀 LPラフ案自動生成システム - 完全ガイド

## ✨ システム完成！

PowerArQ Electric Blanket Liteを使った完全テストが成功しました！

### 🎯 生成されたもの
- **LPラフ案（強化版）**: https://go.docbase.io/posts/3891326
- **レイアウト指示書**: https://go.docbase.io/posts/3891327
- **画像制作チェックリスト**: ローカル生成済み
- **商品データJSON**: 構造化された全商品情報

---

## 🛠️ 4つの使い方

### 1. 🏃‍♂️ 簡単版（規定書CSVから）
```bash
# 仮想環境
source venv/bin/activate
python kishima_spec_to_lp.py "規定書.csv" --upload

# Docker
docker-compose exec lp-generator python kishima_spec_to_lp.py /app/data/規定書.csv --upload
```

### 2. 📊 Excel版
```bash
# テンプレート作成
python excel_to_lp_generator.py --create-template

# Excel編集後に生成
python excel_to_lp_generator.py templates/product.xlsx --upload
```

### 3. 📄 PDF版（準備済み）
```bash
python pdf_to_lp_generator.py data/press_release.pdf --upload
```

### 4. 🎯 **マスター版（おすすめ）**
```bash
# 全機能込み・最高品質
python master_generator.py "入力ファイル" --upload --checklist
```

---

## 💪 システムの強み

### ✅ 他の人でも使える（Docker対応）
- **Docker Compose**で環境統一
- **README_DOCKER.md**に詳しい手順
- **APIトークン設定**だけで即使用可能

### ✅ LPラフ案の精度向上
- **商品カテゴリ自動判定**（electronics/outdoor/lifestyle）
- **カテゴリ別最適化**されたページ構成
- **強化版テンプレート**で詳細情報も完璧
- **規定書の完全活用**（JANコード、型番、仕様等）

### ✅ 画像指示の仕組み
- **8種類の画像タイプ**を自動判定・指示
  - メイン商品画像、ライフスタイル、詳細、比較、シーン、スペック、カラー、ブランド
- **優先度付き**（high/medium/low）
- **具体的撮影指示**付き
- **画像制作チェックリスト**自動生成

### ✅ レイアウト案作成の仕組み
- **6種類のレイアウトパターン**
  - ヒーロー、機能グリッド、比較、ライフスタイル、スペック表、証言
- **業界別最適化**
- **レスポンシブ対応指示**
- **具体的制作指示書**自動生成
- **デザインシステム**（カラー、フォント、スペーシング）

---

## 📋 完全な出力内容

### 1. 強化版LPラフ案
- カテゴリ別最適化されたページ構成
- 詳細な画像指示（優先度付き）
- レイアウトノート
- 制作ガイドライン

### 2. レイアウト指示書  
- ページ別詳細レイアウト案
- 複数案の提示（主案＋代替案）
- レスポンシブ対応指示
- デザインシステム仕様
- 制作ワークフロー

### 3. 画像制作チェックリスト
- 優先度別画像リスト
- 具体的撮影・制作指示
- 品質チェックポイント
- 制作スケジュールテンプレート

### 4. 商品データJSON
- 構造化された全商品情報
- 再利用可能な形式

---

## 🐳 Docker環境での他メンバー利用

### 新しいメンバーの導入（5分）
1. **フォルダをコピー**
2. **Docker Desktopインストール**
3. **`.env`でAPIトークン設定**
4. **`docker-compose up -d`**
5. **完了！**

### 使用方法
```bash
# 基本的な使い方
docker-compose exec lp-generator python master_generator.py /app/data/商品ファイル --upload --checklist

# ファイル確認
docker-compose exec lp-generator ls -la /app/output/
```

---

## 🔧 カスタマイズポイント

### 商品カテゴリ追加
`enhanced_lp_generator.py`の`page_structures`に新しいカテゴリを追加

### レイアウトパターン追加
`layout_generator.py`の`layout_patterns`に新しいパターンを追加

### 画像指示カスタマイズ
`enhanced_lp_generator.py`の`image_templates`を編集

---

## 📊 実績・テスト結果

✅ **PowerArQ Electric Blanket Lite**で完全テスト済み
- 規定書CSV → 完璧なLPラフ案生成
- アウトドアカテゴリ自動判定
- Docbase自動アップロード成功
- レイアウト指示書完全生成
- 画像チェックリスト作成

✅ **Docbase記事**
- LPラフ案: https://go.docbase.io/posts/3891326
- レイアウト指示書: https://go.docbase.io/posts/3891327

---

## 🚀 次のステップ

1. **他の商品でテスト**
2. **チームメンバーでの共有**
3. **Docker環境の配布**
4. **カスタマイズ・機能追加**

このシステムで、LP制作の効率が飛躍的に向上します！🎉