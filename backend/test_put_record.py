import put_record
from datetime import datetime, timedelta
import boto3
import json
import test_utils
from boto3.dynamodb.conditions import Key
import uuid # Import uuid

# テストユーザーIDとテーブル名
user_id = 'testuser001'
table_name = 'MenstruationRecords'
PERIOD_DURATION = 5  # 生理期間（日数）
AVERAGE_CYCLE = 30  # 周期（日数）

def setup_test_data():
    """
    テスト用にテーブルをクリーンアップし、5周期分の生理データを保存。
    """
    print(f"\n--- Setting up test data for {user_id} ---")
    test_utils.delete_table_if_exists(table_name)
    test_utils.create_table_if_not_exists(table_name)

    today_date = test_utils.get_current_date_in_jst()
    # Adjusting for the latest_start_date to ensure recent data
    latest_period_start = today_date - timedelta(days=AVERAGE_CYCLE)

    events_to_put = []

    for i in range(5):  # 5周期分の記録
        start_date = latest_period_start - timedelta(days=AVERAGE_CYCLE * (4 - i))
        end_date = start_date + timedelta(days=PERIOD_DURATION - 1)

        # Create one event per period with both start and end dates
        events_to_put.append({
            'userid': user_id,
            'id': str(uuid.uuid4()), # Generate a unique ID for each period record
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        })

    context = {}

    print(f"Saving {len(events_to_put)} records...")
    for event_data in events_to_put:
        response = put_record.lambda_handler(event_data, context)
        assert response['statusCode'] == 200, f"Error saving record: {response}"
        print(f"Saved record with ID: {json.loads(response['body']).get('record_id')}")

    print("\n--- All records saved ---")
    return events_to_put

if __name__ == '__main__':
    saved_events = setup_test_data()

    # DBから検証用に読み取り
    table = test_utils.dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('userid').eq(user_id)
    )
    retrieved_items = sorted(response['Items'], key=lambda x: x['id'])
    print(f"\nRetrieved {len(retrieved_items)} items from DB after put_record:")
    for item in retrieved_items:
        print(item)

    # Verify that all 5 records (periods) were created and have both start_date and end_date
    assert len(retrieved_items) == 5, f"Expected 5 records, but got {len(retrieved_items)}"
    for item in retrieved_items:
        assert 'start_date' in item, f"Record {item.get('id')} is missing start_date"
        assert 'end_date' in item, f"Record {item.get('id')} is missing end_date"
        assert 'created_at' in item, f"Record {item.get('id')} is missing created_at"
        assert 'updated_at' in item, f"Record {item.get('id')} is missing updated_at"
    
    print("\n✅ put_record test finished successfully.")
