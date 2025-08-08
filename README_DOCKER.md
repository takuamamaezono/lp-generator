# LPラフ案自動生成システム - Docker版

## 🐳 Docker環境での使い方

### 1. 初期設定

```bash
# 1. リポジトリをクローンまたは移動
cd /path/to/lp_generator

# 2. 環境変数ファイルを作成
cp .env.example .env

# 3. .envファイルを編集してDocbase APIトークンを設定
# DOCBASE_ACCESS_TOKEN=your_token_here
# DOCBASE_TEAM=go
```

### 2. Docker起動

```bash
# Dockerコンテナをビルド・起動
docker-compose up -d

# コンテナの状態確認
docker-compose ps
```

### 3. LPラフ案生成

#### 規定書CSVから生成

```bash
# 規定書ファイルをdataフォルダに配置
cp "規定書ファイル.csv" ./data/

# Docker内でスクリプト実行
docker-compose exec lp-generator python kishima_spec_to_lp.py /app/data/規定書ファイル.csv

# Docbaseにアップロードする場合
docker-compose exec lp-generator python kishima_spec_to_lp.py /app/data/規定書ファイル.csv --upload
```

#### Excelファイルから生成

```bash
# Excelテンプレート作成
docker-compose exec lp-generator python excel_to_lp_generator.py --create-template

# Excelファイルから生成
docker-compose exec lp-generator python excel_to_lp_generator.py /app/templates/powerarq_blanket_lite.xlsx --upload
```

### 4. 結果の確認

```bash
# 生成されたファイル確認
ls -la output/

# ログ確認
docker-compose logs lp-generator
```

### 5. Docker終了

```bash
# コンテナ停止
docker-compose down

# 完全削除（データも削除）
docker-compose down -v
```

## 📁 ファイル構成

```
lp_generator/
├── data/           # 入力ファイル（規定書CSV、PDF等）
├── templates/      # テンプレートファイル
├── output/         # 生成されたLPラフ案
├── Dockerfile      # Docker設定
├── docker-compose.yml
├── requirements.txt
└── .env           # 環境変数（APIトークン等）
```

## 🚀 新しいメンバーの導入手順

1. **このフォルダをコピー**
2. **Docker Desktopをインストール**
3. **APIトークンを設定**（.envファイル）
4. **docker-compose up -d**で起動
5. **使い方通りに実行**

## ⚠️ トラブルシューティング

### よくある問題

- **「コンテナが起動しない」** → `docker-compose logs`でログ確認
- **「APIエラー」** → .envファイルのトークン確認
- **「ファイルが見つからない」** → dataフォルダにファイルが配置されているか確認

### 解決方法

```bash
# コンテナ再ビルド
docker-compose build --no-cache
docker-compose up -d

# コンテナ内に入って直接デバッグ
docker-compose exec lp-generator bash
```