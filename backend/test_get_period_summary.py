import get_period_summary
import json

# テストユーザーID
user_id = 'testuser001'

# 過去6ヶ月のサマリーを取得
event_6m = {
    'userId': user_id,
    'span': '6m'
}
context = {}

print(f"\n--- Getting period summary for {user_id} (last 6 months) ---")
response_6m = get_period_summary.lambda_handler(event_6m, context)
summary_6m = response_6m['body']
print(f"Summary (6m): {summary_6m}")

# 過去12ヶ月のサマリーを取得
event_12m = {
    'userId': user_id,
    'span': '12m'
}

print(f"\n--- Getting period summary for {user_id} (last 12 months) ---")
response_12m = get_period_summary.lambda_handler(event_12m, context)
summary_12m = response_12m['body']
print(f"Summary (12m): {summary_12m}")