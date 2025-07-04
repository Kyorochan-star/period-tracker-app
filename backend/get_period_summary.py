import boto3
from datetime import datetime, timedelta

#dynamodb = boto3.resource('dynamodb')
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
    span = event.get('span', '6m')  # '6m' or '12m'

    today = datetime.utcnow()
    if span == '12m':
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=180)

    # 1. データ取得
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(user_id)
    )
    items = response['Items']
    
    # 2. フィルター＆日付ソート
    records = [item for item in items if parse_date(item['recordDate']) >= start_date]
    records.sort(key=lambda x: x['recordDate'])

    # 3. 生理周期まとめ
    periods = []
    current_start = None

    for record in records:
        if record.get('isStart'):
            current_start = parse_date(record['recordDate'])
        elif record.get('isEnd') and current_start:
            end_date = parse_date(record['recordDate'])
            duration = (end_date - current_start).days + 1
            periods.append({
                "start": current_start.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "duration": duration
            })
            current_start = None

    return {
        'statusCode': 200,
        'body': periods
    }

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")
