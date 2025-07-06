import boto3
from botocore.exceptions import ClientError
import time

# DynamoDB LocalのエンドポイントURLを指定
DYNAMODB_ENDPOINT = 'http://localhost:8000'
REGION_NAME = 'ap-northeast-1' # DynamoDB Localではダミーだが、boto3の引数として必要

# DynamoDBクライアントの初期化
dynamodb = boto3.client(
    'dynamodb',
    region_name=REGION_NAME,
    endpoint_url=DYNAMODB_ENDPOINT,
    # ローカル実行時には以下のダミー認証情報を設定することで、
    # 環境変数に依存せずローカルに接続しやすくします。
    # 完了後、コメントアウトまたは削除しても構いません。
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def create_table(table_name, key_schema, attribute_definitions, global_secondary_indexes=None):
    """
    DynamoDBテーブルを作成する汎用関数
    """
    try:
        print(f"テーブル '{table_name}' の作成を開始します...")
        table_params = {
            'TableName': table_name,
            'KeySchema': key_schema,
            'AttributeDefinitions': attribute_definitions,
            'ProvisionedThroughput': { # Localでは無視されることが多いが、形式的に必要
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        }
        if global_secondary_indexes:
            table_params['GlobalSecondaryIndexes'] = global_secondary_indexes

        response = dynamodb.create_table(**table_params)
        print(f"テーブル '{table_name}' の作成リクエストを送信しました。")

        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print(f"テーブル '{table_name}' が正常に作成されました。")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"テーブル '{table_name}' は既に存在します。")
        else:
            print(f"テーブル作成エラー for {table_name}: {e}")
        return None

def main():
    print("DynamoDBテーブル作成スクリプトを開始します。")

    # --- 1. users テーブルの定義と作成 ---
    users_table_name = 'users'
    users_key_schema = [
        {'AttributeName': 'id', 'KeyType': 'HASH'} # パーティションキー
    ]
    users_attribute_definitions = [
        {'AttributeName': 'id', 'AttributeType': 'N'}, # Number型
        {'AttributeName': 'email', 'AttributeType': 'S'} # String型 (GSI用)
    ]
    users_gsi = [
        {
            'IndexName': 'EmailIndex',
            'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        }
    ]
    create_table(users_table_name, users_key_schema, users_attribute_definitions, users_gsi)

    # --- 2. MenstruationRecords テーブルの定義と作成 ---
    menstruation_records_table_name = 'MenstruationRecords'
    menstruation_records_key_schema = [
        {'AttributeName': 'userid', 'KeyType': 'HASH'}, # パーティションキー
        {'AttributeName': 'id', 'KeyType': 'RANGE'} # ソートキー (UUIDなど)
    ]
    menstruation_records_attribute_definitions = [
        {'AttributeName': 'userid', 'AttributeType': 'N'}, # Number型
        {'AttributeName': 'id', 'AttributeType': 'S'}, # String型 (UUIDなど)
        {'AttributeName': 'start_date', 'AttributeType': 'S'} # String型 (GSI用)
    ]
    # オプション: UserStartDateIndex GSI
    menstruation_records_gsi = [
        {
            'IndexName': 'UserStartDateIndex',
            'KeySchema': [
                {'AttributeName': 'userid', 'KeyType': 'HASH'},
                {'AttributeName': 'start_date', 'KeyType': 'RANGE'}
            ],
            'Projection': {'ProjectionType': 'ALL'}, # 必要に応じてINCLUDEで属性を絞る
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        }
    ]
    create_table(menstruation_records_table_name, menstruation_records_key_schema, menstruation_records_attribute_definitions, menstruation_records_gsi)

    print("\nすべてのテーブル作成スクリプトが終了しました。")

if __name__ == "__main__":
    main()