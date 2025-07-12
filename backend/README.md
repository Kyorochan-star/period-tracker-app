# 月経周期トラッカー アプリケーション (バックエンド)

このリポジトリには、月経周期を記録し、次回の生理を予測するバックエンドAPIが含まれています。

## 開発環境のセットアップ

このプロジェクトは Docker と Docker Compose を使用して開発環境を構築します。

### 前提条件

* Docker Desktop (Docker Engine と Docker Compose を含む) がインストールされていること。

### 1. DynamoDB Local (データベース) の起動

アプリケーションが使用するローカルのDynamoDBを起動します。

1.  `backend` ディレクトリに移動します。
    ```bash
    cd backend
    ```

2.  DynamoDB Local サービスを Docker Compose で起動します。
    ```bash
    docker compose up -d dynamodb-local
    ```
    * `-d` オプションはバックグラウンドでコンテナを実行します。
    * このコマンドにより、DynamoDB Local はホストの `8000` 番ポートで利用可能になります。

3.  必要なテーブルを作成します。
    * DynamoDB Local が起動したら、アプリケーションが使用するテーブル (`MenstrualCycles` など) を作成する必要があります。
    ```bash
    python create_tables.py
    ```
    * **注意**: `put_record.py` では `MenstrualCycles` テーブルを使用していますが、`create_tables.py` では `users` と `MenstruationRecords` テーブルを作成するように定義されています。この点、テーブル名が一致しているか確認し、必要に応じて `create_tables.py` または `put_record.py` のテーブル名を修正してください。現在の`put_record.py`は`MenstrualCycles`を使用しているため、`create_tables.py`も`MenstrualCycles`を作成するように変更するか、`put_record.py`のテーブル名を`MenstruationRecords`に合わせる必要があります。

### 2. バックエンドAPIのビルドと起動

FastAPIアプリケーションをDockerコンテナとして起動し、APIエンドポイントを公開します。

1.  `backend` ディレクトリにいることを確認します。
    ```bash
    cd backend
    ```

2.  Docker Compose を使用して、FastAPI アプリケーションのイメージをビルドし、コンテナを起動します。
    ```bash
    docker compose up -d backend-api
    ```
    * このコマンドは、`docker-compose.yml` に定義された `backend-api` サービスをビルドし、起動します。
    * `docker-compose.yml` で `backend-api` サービスがホストの **`8001`** 番ポートにマッピングされていると仮定しています (DynamoDB Local とのポート競合を避けるため)。もし `8000` を使用する場合は、`docker-compose.yml` を確認し、ポートマッピングが競合しないように設定してください。

### 3. APIエンドポイントへのアクセス

FastAPIバックエンドAPIは、以下のURLでアクセス可能です。

* **ルートパス (テスト用):**
    `http://localhost:8001/` (または `http://localhost:8000/`、FastAPIのポートマッピングによる)
    * リクエスト例 (ブラウザでアクセス): `http://localhost:8001/`

* **生理記録の追加と予測:**
    `http://localhost:8001/menstrual-cycles` (または `http://localhost:8000/menstrual-cycles`、FastAPIのポートマッピングによる)
    * **HTTPメソッド**: `POST`
    * **リクエストボディ (JSON)** 例:
        ```json
        {
            "user_id": "user123",
            "start_date": "2025-06-01",
            "end_date": "2025-06-05"
        }
        ```
    * **`curl` コマンドでの実行例:**
        ```bash
        curl -X POST \
             -H "Content-Type: application/json" \
             -d '{"user_id": "user123", "start_date": "2025-06-01", "end_date": "2025-06-05"}' \
             http://localhost:8001/menstrual-cycles
        ```

---

### その他の情報

* **テストの実行**:
    ```bash
    python -m pytest # または python test_put_record.py
    ```
    * テストを実行する前に、DynamoDB Local が起動していることを確認してください。

* **コンテナの停止とクリーンアップ**:
    ```bash
    docker compose down
    ```
    * このコマンドは、`docker-compose.yml` に定義されたすべてのサービスコンテナを停止し、削除します。
    * **注意**: `docker-compose.yml` の `volumes` 設定により、DynamoDB Local のデータは `./docker-dynamodb-data` ディレクトリに永続化されます。データを完全に削除したい場合は、このディレクトリを手動で削除する必要があります。

---

この `README.md` は、プロジェクトのセットアップ、実行、APIの使用方法について、より明確で実践的な情報を提供するはずです。