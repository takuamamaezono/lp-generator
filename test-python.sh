#!/bin/bash

# Pythonパスをテスト
echo "=== Python環境テスト ==="
echo ""

echo "1. システムのPython3:"
which python3
python3 --version
echo ""

echo "2. 仮想環境のactivate:"
if [ -f "/Users/g.ohorudingusu/Docbase/docbase_env/bin/activate" ]; then
    echo "✅ activate found"
    source /Users/g.ohorudingusu/Docbase/docbase_env/bin/activate
    echo "仮想環境のPython:"
    which python
    python --version
else
    echo "❌ activate not found"
fi
echo ""

echo "3. lp_generator.pyの存在:"
if [ -f "/Users/g.ohorudingusu/Docbase/lp_generator/lp_generator.py" ]; then
    echo "✅ lp_generator.py found"
else
    echo "❌ lp_generator.py not found"
fi
echo ""

echo "4. シンプルなPythonテスト:"
/usr/bin/python3 -c "print('Python3 is working!')"