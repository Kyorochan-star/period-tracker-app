import get_records
import json

# テストユーザーID
user_id = 'testuser001'

# 直近180日間のレコードを取得
event_180days = {
    'requestContext': {
        'authorizer': {
            'claims': {
                'sub': user_id
            }
        }
    },
    'queryStringParameters': {
        'days': '180'
    }
}
context = {}

print(f"\n--- Getting records for {user_id} (last 180 days) ---")
response_180days = get_records.lambda_handler(event_180days, context)
items_180days = json.loads(response_180days['body'])
print(f"Found {len(items_180days)} records:")
for item in items_180days:
    print(item)

# 直近30日間のレコードを取得 (クエリパラメータなしのデフォルト動作も確認)
event_30days = {
    'requestContext': {
        'authorizer': {
            'claims': {
                'sub': user_id
            }
        }
    },
    'queryStringParameters': {
        'days': '30'
    }
}

print(f"\n--- Getting records for {user_id} (last 30 days) ---")
response_30days = get_records.lambda_handler(event_30days, context)
items_30days = json.loads(response_30days['body'])
print(f"Found {len(items_30days)} records:")
for item in items_30days:
    print(item)