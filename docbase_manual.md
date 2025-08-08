# 🚀 LPラフ案自動生成システム 操作マニュアル（競合分析版）

## 🎯 システム概要

商品データから**競合分析機能付き**の高品質LPラフ案を自動生成してDocbaseにアップロードする次世代システムです。

### ✨ 最新機能
- **🤖 競合分析AI**: 同一カテゴリ商品の市場分析
- **📊 データドリブン**: 競合データに基づく最適化された訴求
- **📁 マルチフォーマット**: CSV・Excel・PDF対応
- **🐳 Docker**: 環境構築不要で即利用
- **👥 チーム対応**: GitHub共有で全員利用可能

### 📦 生成されるもの
- **競合分析レポート**（市場データ・価格分析・成功パターン）
- **強化版LPラフ案**（競合データ反映・差別化明確）
- **通常版LPラフ案**（従来の10ページ構成）
- **商品情報**（SKU・JAN・仕様・セールスポイント）

---

## 🚀 基本的な使い方

### 1. 事前準備
1. **規定書CSVファイル**を用意
2. **Docbase APIトークン**を取得
3. **システムの起動**（Docker推奨）

### 2. 実行コマンド

#### 🌟 競合分析強化版（推奨）
```bash
# 競合分析付き最高品質LP生成
docker-compose exec lp-generator python advanced_lp_generator.py /app/data/商品データ.csv --upload --analysis

# 生成のみ（アップロードなし）
docker-compose exec lp-generator python advanced_lp_generator.py /app/data/商品データ.csv --analysis
```

#### 📊 通常版（高速）
```bash
# 従来の高速生成
docker-compose exec lp-generator python correct_lp_generator.py /app/data/商品データ.csv --upload
```

#### 📁 対応フォーマット
```bash
# CSV形式
docker-compose exec lp-generator python advanced_lp_generator.py /app/data/商品.csv --analysis

# Excel形式
docker-compose exec lp-generator python excel_to_lp_generator.py /app/data/商品.xlsx --upload

# PDF形式（プレスリリース）
docker-compose exec lp-generator python pdf_to_lp_generator.py /app/data/リリース.pdf --upload
```

### 3. 結果確認
- **📊 競合分析レポート**: `output/competitor_report_商品名_日時.md`
- **🚀 強化版LP**: `output/lp_rough_enhanced_商品名_日時.md`
- **📝 通常LP**: `output/lp_rough_商品名_日時.md`
- **🌐 Docbase URL**: コンソールに表示

---

## 🐳 Docker環境でのセットアップ

### 初回セットアップ（5分）

#### 1. システムファイルの取得
```bash
# GitHubからクローン
git clone https://github.com/YOUR_USERNAME/lp-generator.git
cd lp-generator
```

#### 2. APIトークンの設定
```bash
# 環境変数ファイルをコピー
cp .env.example .env

# .envファイルを編集
# DOCBASE_ACCESS_TOKEN=your_docbase_token_here
# DOCBASE_TEAM=go
```

#### 3. Docker起動
```bash
# システム起動
docker-compose up -d

# 正常起動確認
docker-compose ps
```

### 日常利用

#### 1. 規定書ファイルの配置
```bash
# dataフォルダに規定書CSVをコピー
cp "規定書ファイル.csv" ./data/
```

#### 2. LPラフ案生成
```bash
# 生成 + Docbaseアップロード
docker-compose exec lp-generator python correct_lp_generator.py /app/data/規定書ファイル.csv --upload

# 生成のみ（アップロードしない）
docker-compose exec lp-generator python correct_lp_generator.py /app/data/規定書ファイル.csv
```

#### 3. 結果確認
```bash
# 生成されたファイル確認
docker-compose exec lp-generator ls -la /app/output/

# ログ確認
docker-compose logs lp-generator
```

---

## 📋 データファイルの要件

### CSV形式（Kishima規定書）
#### 必須情報
- **商品名**: 商品の正式名称
- **商品名カナ**: カタカナ表記  
- **メーカー型番**: 商品の型番
- **JANコード（バリエーション別）**: `ブラック：4571427130640`
- **商品サイズ**: サイズ情報
- **重量**: 商品重量
- **定格**: 電源仕様等
- **セールスポイント**: `●`から始まる特徴一覧

### Excel形式
#### サポート構成
- **複数シート対応**: 商品情報・仕様・価格シート等
- **自動セル抽出**: 商品名・価格・特徴を自動認識
- **フォーマット自由**: 多様なExcel形式に対応

### PDF形式（プレスリリース）
#### 対応内容
- **商品発表資料**: 新商品のプレスリリース
- **技術仕様書**: 詳細スペック資料
- **マーケティング資料**: 売り込み資料

### フォーマット例
```
商品名,PowerArQ Electric Blanket Lite
JANコード（バリエーション別）,ブラック：4571427130640
,ベージュ：4571427130657
セールスポイント,●10段階の温度調節
,●過熱保護システム搭載
```

---

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 「コンテナが起動しない」
```bash
# ログ確認
docker-compose logs

# 再ビルド
docker-compose build --no-cache
docker-compose up -d
```

#### 「APIエラー」
- `.env`ファイルのトークンを確認
- Docbaseのアクセス権限を確認

#### 「ファイルが見つからない」
- `data`フォルダにファイルが配置されているか確認
- ファイル名に日本語や特殊文字が含まれていないか確認

#### 「商品情報が正しく抽出されない」
- 規定書CSVのフォーマットを確認
- 必須項目が全て含まれているか確認

### ヘルプコマンド
```bash
# 使用方法を表示
docker-compose exec lp-generator python correct_lp_generator.py --help

# システム状態確認
docker-compose ps
docker-compose exec lp-generator ls -la /app/
```

---

## 📊 生成されるLPラフ案の構成

### ページ構成（全10ページ）
1. **TOPキャッチ**: 商品名・主要機能
2. **売れている訴求・実績**: ブランド実績
3. **ブランド価値・安全性**: PowerARQブランド
4. **メイン機能・特徴1**: 10段階温度調節
5. **メイン機能・特徴2**: 過熱保護・安全性
6. **使用シーン**: キャンプ・アウトドア等
7. **サイズ・スペック詳細**: 仕様情報
8. **付属品・同梱物**: コントローラー等
9. **保証・アフターサービス**: サポート体制
10. **よくある質問**: FAQ

### 各ページの構成
- **レイアウト案**: デザイン指示
- **テキスト**: 記載内容
- **使用画像**: 画像指示

---

## 🎯 効果的な活用方法

### 1. 複数商品の一括処理
```bash
# 複数ファイルを順次処理
for file in data/*.csv; do
  docker-compose exec lp-generator python correct_lp_generator.py "/app/$file" --upload
done
```

### 2. 定期実行の設定
```bash
# cronで定期実行（例：毎日9時）
0 9 * * * cd /path/to/lp-generator && docker-compose exec -T lp-generator python correct_lp_generator.py /app/data/latest.csv --upload
```

### 3. バックアップ運用
```bash
# 生成ファイルのバックアップ
docker-compose exec lp-generator tar -czf /app/backup_$(date +%Y%m%d).tar.gz /app/output/
```

---

## 📞 サポート・問い合わせ

### システムに関する問題
1. **GitHub Issues**: バグ報告・機能要望
2. **Docbase**: 運用に関する相談
3. **チームSlack**: 緊急時の連絡

### システム更新
```bash
# 最新版の取得
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```

---

## 📈 今後の機能拡張

### 実装済み機能 ✅
- [x] **競合分析AI**: 市場データ分析・最適化提案
- [x] **Excel形式対応**: 複数シート・多様フォーマット
- [x] **PDF形式対応**: プレスリリース・技術資料
- [x] **Docker完全対応**: 環境構築不要
- [x] **GitHub共有**: チーム全体での利用

### 今後の機能拡張
- [ ] **AI画像生成連携**: 商品画像の自動生成
- [ ] **リアルタイム競合監視**: 市場変動の自動検知
- [ ] **A/Bテスト機能**: 複数LP案の自動生成
- [ ] **多言語対応**: 英語・中国語LP対応
- [ ] **Webインターフェース**: ブラウザでの操作画面

システムの改善要望や新機能のリクエストがあれば、GitHubのIssuesまたはDocbaseでお知らせください。

---

**🎉 以上でLPラフ案自動生成システムの操作マニュアルは完了です！**