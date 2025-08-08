# LPラフ案自動生成システム 操作マニュアル

## 🎯 システム概要

規定書CSVから自動でLPラフ案を生成してDocbaseにアップロードするシステムです。

### ✨ 特徴
- 規定書CSV → 1コマンド → 完成したLPラフ案
- 商品情報（SKU・JAN、仕様、セールスポイント）を自動抽出
- Docbaseに自動アップロード
- Docker対応で誰でも使える

### 📦 生成されるもの
- **LPラフ案**（10ページ構成）
- **商品名・SKU・JAN情報**
- **規定書の全情報を反映**

---

## 🚀 基本的な使い方

### 1. 事前準備
1. **規定書CSVファイル**を用意
2. **Docbase APIトークン**を取得
3. **システムの起動**（Docker推奨）

### 2. 実行コマンド
```bash
# ローカル環境（上級者向け）
python correct_lp_generator.py "規定書ファイル.csv" --upload

# Docker環境（推奨）
docker-compose exec lp-generator python correct_lp_generator.py /app/data/規定書ファイル.csv --upload
```

### 3. 結果確認
- **コンソール**にDocbase URLが表示されます
- **outputフォルダ**にMarkdownファイルが生成されます

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

## 📋 規定書CSVの要件

### 必須情報
- **商品名**: 商品の正式名称
- **商品名カナ**: カタカナ表記
- **メーカー型番**: 商品の型番
- **JANコード（バリエーション別）**: カラー別JANコード
- **商品サイズ**: サイズ情報
- **重量**: 商品重量
- **定格**: 電源仕様等
- **セールスポイント**: ●から始まる特徴一覧

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

### 予定機能
- [ ] Excel形式の規定書サポート
- [ ] PDF形式のプレスリリース対応
- [ ] 画像自動取得機能
- [ ] レイアウト案の自動生成
- [ ] 多言語対応

システムの改善要望や新機能のリクエストがあれば、GitHubのIssuesまたはDocbaseでお知らせください。

---

**🎉 以上でLPラフ案自動生成システムの操作マニュアルは完了です！**