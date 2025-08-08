#!/bin/bash

# LPラフ案生成システム起動スクリプト

echo "🚀 LPラフ案生成システムを起動します..."

# ディレクトリ移動
cd "$(dirname "$0")"

# 仮想環境を有効化
source ../docbase_env/bin/activate

# Pythonスクリプトを実行
python lp_rough_generator.py

echo ""
echo "✅ 処理が完了しました"