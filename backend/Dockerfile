# Docker Hubからpythonという公開イメージのバージョン3.11をとってくる 
FROM python:3.11

# 作業ディレクトリを決める(このフォルダの中で以降の作業をしてください)
WORKDIR /app

# requirements.txtをコピーしてライブラリインストール
COPY requirements.txt .
# 「イメージを作るときに実行」
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . .

# アプリを起動（FastAPI）
# CMDは「Dockerコンテナを起動したとき」に自動的に実行されるコマンド
# --host を指定するとPCだけでなく、外からのアクセスが可能になる
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
