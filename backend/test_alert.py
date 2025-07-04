import alert
import json

# テストユーザーID
user_id = 'testuser001'

# 最新の生理開始日を仮定
event = {
    'userId': user_id,
    'recordDate': '2024-05-04' # put-record.pyで最後に記録した生理開始日
}
context = {}

print(f"\n--- Simulating alert for {user_id} ---")
alert.send_period_prediction(event, context)
print("Alert simulation completed. Check console output for message.")