import boto3
from datetime import datetime, date, timedelta
import uuid
import json

# DynamoDB Localの設定
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='ap-northeast-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)
table = dynamodb.Table('MenstrualCycles')

# デフォルト値の定義
DEFAULT_CYCLE_LENGTH = 30 # デフォルトの周期 (日)
DEFAULT_PERIOD_LENGTH = 5 # デフォルトの生理期間 (日)

def calculate_prediction(records):
    """
    過去の生理記録から平均周期と次回の生理予測日を計算します。
    records: 生理記録のリスト（start_dateとend_dateを含む）
    生理記録がない場合や少ない場合はデフォルト値を使用します。
    """
    # start_dateでソート（昇順）
    sorted_records = sorted(records, key=lambda x: datetime.strptime(x['start_date'], '%Y-%m-%d'))
    history_count = len(sorted_records)

    # 履歴が全くない場合、予測はできません
    if history_count == 0:
        return None, None, None, 0

    # 最新の生理記録を取得
    latest_record = sorted_records[-1]
    latest_start_date = datetime.strptime(latest_record['start_date'], '%Y-%m-%d').date()
    latest_end_date = datetime.strptime(latest_record['end_date'], '%Y-%m-%d').date()

    # 生理期間の長さは、最新の記録から計算します
    period_length = (latest_end_date - latest_start_date).days + 1

    # 履歴が1つだけの場合：デフォルト周期を使用
    if history_count == 1:
        average_cycle_length = DEFAULT_CYCLE_LENGTH
        predicted_next_start_date = latest_start_date + timedelta(days=average_cycle_length)
        predicted_end_date = predicted_next_start_date + timedelta(days=period_length - 1)
        
        return predicted_next_start_date.strftime('%Y-%m-%d'), \
               predicted_end_date.strftime('%Y-%m-%d'), \
               average_cycle_length, \
               history_count

    # 履歴が2つ以上の場合：過去の周期の平均を使用
    cycle_lengths = []
    for i in range(len(sorted_records) - 1):
        current_cycle_start = datetime.strptime(sorted_records[i]['start_date'], '%Y-%m-%d').date()
        next_cycle_start = datetime.strptime(sorted_records[i+1]['start_date'], '%Y-%m-%d').date()
        cycle_lengths.append((next_cycle_start - current_cycle_start).days)
    
    # 周期長のリストが空になることは、このロジックでは通常発生しませんが、念のため
    if not cycle_lengths:
        average_cycle_length = DEFAULT_CYCLE_LENGTH # フォールバックとしてデフォルトを使用
    else:
        average_cycle_length = sum(cycle_lengths) // len(cycle_lengths)

    predicted_next_start_date = latest_start_date + timedelta(days=average_cycle_length)
    predicted_end_date = predicted_next_start_date + timedelta(days=period_length - 1)

    return predicted_next_start_date.strftime('%Y-%m-%d'), \
           predicted_end_date.strftime('%Y-%m-%d'), \
           average_cycle_length, \
           history_count

def lambda_handler(event, context):
    """
    API Gatewayからのイベントを受け取り、生理記録をDynamoDBに保存し、予測結果を返します。
    """
    try:
        # イベントから必要なデータを取得
        user_id = event.get('user_id')
        start_date_str = event.get('start_date')
        end_date_str = event.get('end_date')

        # 必須フィールドのバリデーション
        if not user_id or not start_date_str or not end_date_str:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'user_id, start_date, and end_date are required.'})
            }

        record_id = str(uuid.uuid4())
        current_time_utc = datetime.utcnow()

        # DynamoDBに保存するアイテムを準備
        item = {
            'id': record_id, # ユニークなレコードID
            'user_id': user_id, # ユーザー識別子
            'start_date': start_date_str, # 生理開始日
            'end_date': end_date_str,     # 生理終了日
            'created_at': current_time_utc.strftime("%Y-%m-%d"), # 記録作成日 (日付のみ)
            'updated_at': current_time_utc.isoformat() # 最終更新日時 (ISO 8601形式)
        }

        # 予測のために、当該user_idの全生理記録をDynamoDBから取得
        # 'user_id-start_date-index' というGSI (Global Secondary Index) が必要です
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id),
            IndexName='user_id-start_date-index' 
        )
        existing_records = response.get('Items', [])
        
        # 今回追加する新しい記録も予測計算に含めます
        all_records_for_prediction = existing_records + [{
            'start_date': start_date_str,
            'end_date': end_date_str
        }]

        # 予測計算の実行
        predicted_start_date, predicted_end_date, average_cycle, history_count = calculate_prediction(all_records_for_prediction)

        # 予測結果があれば、アイテムに追加
        if predicted_start_date:
            item['prediction_next_start_date'] = predicted_start_date
        if predicted_end_date:
            item['prediction_end_date'] = predicted_end_date

        # DynamoDBにアイテムを保存
        table.put_item(Item=item)

        # 予測結果を含むレスポンスボディを準備
        response_body = {
            'message': '記録を保存しました',
            'record_id': record_id,
            'averageCycle': average_cycle,
            'historyCount': history_count,
            'predictedStartDate': predicted_start_date,
            'predictedEndDate': predicted_end_date
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_body) # JSON形式でレスポンスを返す
        }

    except Exception as e:
        # エラー発生時のハンドリング
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)}) # エラーメッセージをJSONで返す
        }