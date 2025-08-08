FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 依存関係をコピーしてインストール
COPY requirements_pdf.txt .
RUN pip install --no-cache-dir -r requirements_pdf.txt

# 追加でopenpyxlもインストール
RUN pip install --no-cache-dir openpyxl==3.1.5

# アプリケーションファイルをコピー
COPY *.py ./
COPY templates/ ./templates/
COPY run_*.sh ./

# アプリケーション用のユーザーを作成
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# デフォルトコマンド
CMD ["python", "lp_rough_generator.py"]