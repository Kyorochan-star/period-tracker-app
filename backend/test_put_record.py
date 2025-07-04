import put_record
from datetime import datetime, timedelta

# テストユーザーID
user_id = 'testuser001'

# データを複数回保存して、予測や履歴のためのデータを用意する
# 生理開始日を記録 (isStart=True を設定)
events_to_put = [
    # 過去の生理開始日
    {'userId': user_id, 'recordDate': '2024-01-01', 'mood': 'normal', 'isStart': True},
    {'userId': user_id, 'recordDate': '2024-01-05', 'mood': 'tired', 'isEnd': True},
    {'userId': user_id, 'recordDate': '2024-02-01', 'mood': 'happy', 'isStart': True}, # 31日周期
    {'userId': user_id, 'recordDate': '2024-02-05', 'mood': 'ok', 'isEnd': True},
    {'userId': user_id, 'recordDate': '2024-03-03', 'mood': 'angry', 'isStart': True}, # 31日周期
    {'userId': user_id, 'recordDate': '2024-03-07', 'mood': 'sad', 'isEnd': True},
    {'userId': user_id, 'recordDate': '2024-04-03', 'mood': 'good', 'isStart': True}, # 31日周期
    {'userId': user_id, 'recordDate': '2024-04-07', 'mood': 'neutral', 'isEnd': True},
    # 最新の生理開始日
    {'userId': user_id, 'recordDate': '2024-05-04', 'mood': 'excited', 'isStart': True}, # 31日周期
    {'userId': user_id, 'recordDate': '2024-05-08', 'mood': 'calm', 'isEnd': True},
    # その他の記録
    {'userId': user_id, 'recordDate': '2024-05-15', 'symptoms': ['headache']},
    {'userId': user_id, 'recordDate': '2024-05-20', 'note': 'ピルを服用'},
]

context = {} # ローカルテスト用の空のコンテキスト

for i, event_data in enumerate(events_to_put):
    print(f"Saving record {i+1} for {event_data['recordDate']}...")
    response = put_record.lambda_handler(event_data, context)
    print(f"Response: {response}")

print("\n--- All records saved ---")