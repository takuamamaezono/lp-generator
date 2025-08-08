#!/bin/bash

# LP欄生成システム実行スクリプト
# 使い方: ./run_lp_generator.sh

echo "================================"
echo "    LP欄生成システム 起動"
echo "================================"
echo ""

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# Docbaseの仮想環境を有効化
echo "🔧 環境準備中..."
source ../docbase_env/bin/activate

# テンプレートディレクトリの存在確認
if [ ! -d "templates" ] || [ -z "$(ls -A templates)" ]; then
    echo "📋 テンプレートを作成します..."
    python create_templates.py
    echo ""
fi

# メインスクリプトを実行
echo "🚀 LP欄生成システムを起動します..."
echo ""
python lp_generator.py

# 生成されたファイルの確認
echo ""
echo "================================"
echo "最近生成されたLP欄:"
ls -lt output/ 2>/dev/null | head -6 | tail -5

# Docbaseアップロードの案内
echo ""
echo "💡 Docbaseにアップロードする場合:"
echo "   python docbase_lp_uploader.py output/[ファイル名]"
echo ""
echo "================================"