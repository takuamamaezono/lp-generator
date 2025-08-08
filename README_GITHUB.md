# 📄 Docbase LPラフ案自動生成システム

商品データを入力するだけで、Docbase用のLPラフ案を自動生成するツールです。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)

## ✨ 特徴

- 🚀 **簡単操作** - 対話式入力で誰でも使える
- 📋 **テンプレート対応** - JSONテンプレートで効率化
- 🖼️ **画像管理** - 画像がない場合は「準備中」を自動表示
- 🔄 **Docbase連携** - 生成したLPを直接アップロード
- 🐳 **Docker対応** - 環境構築不要ですぐ使える

## 📸 スクリーンショット

<details>
<summary>実行画面</summary>

```
🚀 LPラフ案自動生成システム
==================================================

起動モードを選択してください:
1. 新規作成
2. テンプレートから作成
3. JSONファイルから読み込み

選択 (1-3): 1

📝 商品情報を入力してください
----------------------------------------
商品名 (必須): ICEBERG 12L
作成の目的・意図: 新商品ローンチのためのLP作成
```
</details>

## 🚀 クイックスタート

### Docker版（推奨）

```bash
# 1. クローン
git clone https://github.com/your-org/docbase-lp-generator.git
cd docbase-lp-generator

# 2. 環境設定
cp .env.example .env
# .envファイルを編集してAPIトークンを設定

# 3. 起動
docker-compose up -d

# 4. 実行
docker-compose exec lp-generator python lp_rough_generator.py
```

### ローカル版

```bash
# 1. セットアップ
pip install -r requirements.txt

# 2. 環境設定
cp .env.example .env
# APIトークンを設定

# 3. 実行
python lp_rough_generator.py
```

## 📝 使い方

### 対話式入力
```bash
python lp_rough_generator.py
```

### JSONテンプレートから生成
```bash
python lp_rough_generator.py templates/lp_rough_template.json
```

### サンプルJSON
```json
{
  "product_name": "ICEBERG 12L",
  "purpose": "新商品ローンチのためのLP作成",
  "sku_list": [
    {
      "type": "コヨーテタン",
      "sku": "A0057",
      "jan": "4571427130572"
    }
  ],
  "catch_copy": "持ち運べる冷凍・冷蔵庫"
}
```

## 📁 プロジェクト構成

```
docbase-lp-generator/
├── lp_rough_generator.py    # メインスクリプト
├── docbase_lp_uploader.py   # Docbaseアップローダー
├── templates/               # テンプレート
│   └── lp_rough_template.json
├── output/                  # 生成ファイル
├── docker-compose.yml       # Docker設定
├── requirements.txt         # Python依存関係
└── .env.example            # 環境変数サンプル
```

## 🔧 設定

### 必要な環境変数

```env
# Docbase APIトークン
DOCBASE_ACCESS_TOKEN=your_token_here

# Docbaseチーム名
DOCBASE_TEAM=your_team
```

### APIトークンの取得

1. Docbaseにログイン
2. 設定 → APIトークン
3. 新規発行
4. トークンをコピーして`.env`に設定

## 🐳 Docker

### ビルド
```bash
docker-compose build
```

### 起動
```bash
docker-compose up -d
```

### ログ確認
```bash
docker-compose logs -f
```

## 🤝 コントリビューション

プルリクエスト歓迎です！

1. Fork it
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 ライセンス

MIT License - 詳細は[LICENSE](LICENSE)を参照

## 🆘 サポート

- [Issues](https://github.com/your-org/docbase-lp-generator/issues) - バグ報告・機能要望
- [Discussions](https://github.com/your-org/docbase-lp-generator/discussions) - 質問・議論

## 👥 著者

- [@g.ohorudingusu](https://github.com/g-ohorudingusu)

## 🙏 謝辞

- [Docbase](https://docbase.io) - 素晴らしいドキュメント管理ツール
- すべてのコントリビューター