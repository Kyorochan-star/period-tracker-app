import boto3
import os
from datetime import datetime

#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table(os.environ['TABLE_NAME'])
# ← ファイルの先頭付近
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',         # ← 追加
    region_name='ap-northeast-1',                 # ← 追加
    aws_access_key_id='dummy',                    # ← 追加
    aws_secret_access_key='dummy'                 # ← 追加
)

table = dynamodb.Table('Records')  


def lambda_handler(event, context):
    user_id = event['userId']
    record_date = event['recordDate']  # 例: '2025-07-02'
    mood = event.get('mood', '')
    symptoms = event.get('symptoms', [])
    note = event.get('note', '')
    mode_used = event.get('modeUsed', 'default')

    item = {
        'userId': user_id,
        'recordDate': record_date,
        'mood': mood,
        'symptoms': symptoms,
        'note': note,
        'modeUsed': mode_used,
        'timestamp': datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': '記録を保存しました'
    }
