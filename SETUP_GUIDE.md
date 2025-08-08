# Docbase LPラフ案生成システム セットアップガイド

## 概要
商品データからDocbase用のLPラフ案を自動生成するシステムです。  
DockerまたはPython環境で動作し、チーム全体で利用可能です。

## 必要なもの

- **Docbase APIトークン**（必須）
- **Docker** または **Python 3.9以上**
- **Git**（ソースコード取得用）

---

## 🚀 クイックスタート（Docker版）推奨

### 1. リポジトリをクローン
```bash
git clone https://github.com/your-org/docbase-lp-generator.git
cd docbase-lp-generator
```

### 2. 環境変数を設定
```bash
# .env.exampleをコピー
cp .env.example .env

# .envファイルを編集
# DOCBASE_ACCESS_TOKEN と DOCBASE_TEAM を設定
vi .env
```

### 3. Dockerコンテナを起動
```bash
# ビルドして起動
docker-compose up -d

# 対話式でLP生成
docker-compose exec lp-generator python lp_rough_generator.py

# またはJSONから生成
docker-compose exec lp-generator python lp_rough_generator.py templates/lp_rough_template.json
```

---

## 💻 ローカル環境での設定（Docker不要版）

### 1. Python環境の準備
```bash
# Python 3.9以上が必要
python --version

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Mac/Linux
# または
venv\Scripts\activate  # Windows
```

### 2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定
```bash
cp .env.example .env
# .envファイルを編集してAPIトークンを設定
```

### 4. 実行
```bash
# 対話式
python lp_rough_generator.py

# JSONテンプレートから
python lp_rough_generator.py templates/lp_rough_template.json
```

---

## 📝 Docbase APIトークンの取得方法

1. Docbaseにログイン
2. 設定 → 個人設定 → APIトークン
3. 「新規発行」をクリック
4. メモに「LP生成システム用」など記入
5. 発行されたトークンをコピー
6. `.env`ファイルの`DOCBASE_ACCESS_TOKEN`に設定

参考: https://help.docbase.io/posts/45703

---

## 🎯 使用方法

### 対話式で商品情報を入力

1. スクリプトを実行
2. メニューから選択:
   - `1. 新規作成` - ゼロから入力
   - `2. テンプレートから作成` - 既存テンプレートを使用
   - `3. JSONファイルから読み込み` - 商品データJSONを使用
3. 必要な情報を入力
4. LPラフ案が`output/`フォルダに生成される
5. Docbaseへのアップロードも可能

### JSONテンプレートで一括生成

```json
{
  "product_name": "ICEBERG 12L",
  "purpose": "新商品ローンチのためのLP作成",
  "target_platform": "楽天以外のECサイト",
  "sku_list": [
    {
      "type": "コヨーテタン",
      "sku": "A0057",
      "jan": "4571427130572"
    }
  ],
  "catch_copy": "持ち運べる冷凍・冷蔵庫",
  "main_features": "最大冷却 -20℃"
}
```

---

## 📁 フォルダ構成

```
docbase-lp-generator/
├── templates/           # 商品テンプレート
│   └── lp_rough_template.json
├── output/             # 生成されたLPラフ案
├── data/              # 商品データ（オプション）
├── .env               # 環境変数（要作成）
└── docker-compose.yml # Docker設定
```

---

## 🔧 カスタマイズ

### テンプレートの追加

1. `templates/`フォルダに新しいJSONファイルを作成
2. 既存のテンプレートを参考に編集
3. スクリプト実行時に選択可能になる

### デフォルト構成の変更

`lp_rough_generator.py`の`_generate_default_pages`メソッドを編集

---

## ⚠️ トラブルシューティング

### APIトークンエラー
```
❌ エラー: DOCBASE_ACCESS_TOKENが設定されていません
```
→ `.env`ファイルにトークンを設定

### Docker起動エラー
```bash
# コンテナを再ビルド
docker-compose build --no-cache
docker-compose up -d
```

### 権限エラー
```bash
# outputフォルダの権限を変更
chmod 755 output/
chmod 755 templates/
```

---

## 👥 チームでの利用

### 管理者向け

1. GitHubリポジトリを作成
2. このコードをプッシュ
3. チームメンバーに共有
4. 各メンバーが自分のAPIトークンを設定

### 利用者向け

1. リポジトリをクローン
2. APIトークンを取得・設定
3. Dockerで起動
4. LP生成を実行

---

## 📧 サポート

問題が発生した場合：
1. このドキュメントを確認
2. GitHubのIssuesで報告
3. 管理者に連絡

---

## 🔐 セキュリティ注意事項

- **APIトークンは絶対に共有しない**
- `.env`ファイルはGitにコミットしない
- 定期的にトークンを更新する
- 不要になったトークンは削除する