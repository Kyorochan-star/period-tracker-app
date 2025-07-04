import boto3

# DynamoDB Local に接続
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='ap-northeast-1',
    aws_access_key_id='fakeMyKeyId',
    aws_secret_access_key='fakeSecretAccessKey'
)

# テーブル作成
table_name = 'TestTable'
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # パーティションキー
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'  # 文字列
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
    print(f"✅ Created table {table_name}")
except Exception as e:
    print(f"⚠️  Table creation skipped: {e}")

# データを挿入
table = dynamodb.Table(table_name)
table.put_item(
    Item={
        'id': '001',
        'message': 'Hello, DynamoDB Local!'
    }
)
print("✅ Item inserted")

# データを取得
response = table.get_item(Key={'id': '001'})
item = response.get('Item')
print(f"📦 Retrieved item: {item}")

