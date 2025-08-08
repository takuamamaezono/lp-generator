# Docbase LP Generator Makefile

.PHONY: help build up down restart logs shell clean test

help: ## ヘルプを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Dockerイメージをビルド
	docker-compose build

up: ## コンテナを起動
	docker-compose up -d

down: ## コンテナを停止
	docker-compose down

restart: down up ## コンテナを再起動

logs: ## ログを表示
	docker-compose logs -f

shell: ## コンテナにシェルアクセス
	docker-compose exec lp-generator /bin/bash

run: ## LP生成を実行（対話式）
	docker-compose exec lp-generator python lp_rough_generator.py

run-template: ## テンプレートからLP生成
	docker-compose exec lp-generator python lp_rough_generator.py templates/lp_rough_template.json

clean: ## outputフォルダをクリーンアップ
	rm -f output/*.md
	rm -f output/*.json

test: ## テスト実行
	docker-compose exec lp-generator python -m pytest tests/

setup: ## 初期セットアップ
	@echo "セットアップを開始します..."
	@cp -n .env.example .env 2>/dev/null || echo ".envファイルは既に存在します"
	@mkdir -p output templates data
	@echo "セットアップ完了！"
	@echo ".envファイルを編集してAPIトークンを設定してください"

local-run: ## ローカル環境で実行（Docker不要）
	python lp_rough_generator.py

local-install: ## ローカル環境の依存関係をインストール
	pip install -r requirements.txt