import json
from datetime import datetime, timedelta, date
import uuid
import test_utils # DynamoDB操作ヘルパー関数を含むファイル
import put_record # Lambdaハンドラが定義されているファイル

# テストユーザーID (DynamoDBのパーティションキーがStringなので文字列で定義)
user_id_default_test = 'testuser_default_predict_001' # デフォルト予測テスト用
user_id_combined_test = 'testuser_predict_001'      # 複数記録予測テスト用

# put_record.py と同じデフォルト値を参照
DEFAULT_CYCLE_LENGTH = put_record.DEFAULT_CYCLE_LENGTH
DEFAULT_PERIOD_LENGTH = put_record.DEFAULT_PERIOD_LENGTH

# 複数記録テスト用の設定
TEST_CYCLE_LENGTH_1 = 28 # 1回目の生理周期
TEST_CYCLE_LENGTH_2 = 32 # 2回目の生理周期
TEST_PERIOD_LENGTH = 7   # テストで使用する生理期間の長さ (これはput_record.pyのDEFAULT_PERIOD_LENGTHとは別)

# --- test_utils.py にあるべきヘルパー関数の想定 ---
# 以下は test_utils.py に含まれていることを想定しています。
# from datetime import datetime, date, timedelta
# import boto3
# import pytz # 必要に応じて pytz をインストール: pip install pytz

# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='ap-northeast-1',
#     aws_access_key_id='dummy',
#     aws_secret_access_key='dummy'
# )
# table = dynamodb.Table('MenstrualCycles') # MenstrualCycles テーブルを使用

# def create_table_if_not_exists():
#     """DynamoDBテーブルが存在しない場合、GSIと共に作成します。"""
#     try:
#         table.load()
#         print("Table 'MenstrualCycles' already exists.")
#     except boto3.client_error.exceptions.ResourceNotFoundException:
#         print("Creating table 'MenstrualCycles'...")
#         table = dynamodb.create_table(
#             TableName='MenstrualCycles',
#             KeySchema=[
#                 {'AttributeName': 'id', 'KeyType': 'HASH'}
#             ],
#             AttributeDefinitions=[
#                 {'AttributeName': 'id', 'AttributeType': 'S'},
#                 {'AttributeName': 'user_id', 'AttributeType': 'S'},
#                 {'AttributeName': 'start_date', 'AttributeType': 'S'}
#             ],
#             ProvisionedThroughput={
#                 'ReadCapacityUnits': 5,
#                 'WriteCapacityUnits': 5
#             },
#             GlobalSecondaryIndexes=[
#                 {
#                     'IndexName': 'user_id-start_date-index', # ユーザーIDと開始日でクエリ・ソートするためのGSI
#                     'KeySchema': [
#                         {'AttributeName': 'user_id', 'KeyType': 'HASH'},
#                         {'AttributeName': 'start_date', 'KeyType': 'RANGE'}
#                     ],
#                     'Projection': {
#                         'ProjectionType': 'ALL' # 全属性を投影 (必要に応じて変更)
#                     },
#                     'ProvisionedThroughput': {
#                         'ReadCapacityUnits': 5,
#                         'WriteCapacityUnits': 5
#                     }
#                 }
#             ]
#         )
#         table.wait_until_exists()
#         print("Table 'MenstrualCycles' created successfully.")
#
# def clear_table_data(user_id):
#     """指定されたuser_idの全データをクリアします。"""
#     print(f"Clearing data for user_id: {user_id}...")
#     records = get_all_records(user_id)
#     with table.batch_writer() as batch:
#         for record in records:
#             batch.delete_item(
#                 Key={
#                     'id': record['id']
#                 }
#             )
#     print("Data cleared.")
#
# def get_all_records(user_id):
#     """指定されたuser_idの全ての生理記録をGSIを使って取得します。"""
#     try:
#         response = table.query(
#             IndexName='user_id-start_date-index',
#             KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
#         )
#         return response.get('Items', [])
#     except Exception as e:
#         print(f"Error getting all records for user {user_id}: {e}")
#         return []
#
# def get_record_by_id(user_id, record_id):
#     """指定されたrecord_idを持つレコードをDynamoDBから取得します。
#     idがプライマリキーなのでget_itemを使いますが、user_idが一致するか確認します。
#     """
#     try:
#         response = table.get_item(
#             Key={
#                 'id': record_id
#             }
#         )
#         item = response.get('Item')
#         if item and item.get('user_id') == user_id:
#             return item
#         return None
#     except Exception as e:
#         print(f"Error getting record by ID {record_id}: {e}")
#         return None
#
# def get_current_date_in_jst():
#     """現在のJST日付をdatetime.dateオブジェクトで返します。"""
#     # ローカル環境のJST設定を前提とするか、pytzを使用
#     try:
#         jst = pytz.timezone('Asia/Tokyo')
#         return datetime.now(jst).date()
#     except NameError:
#         # pytz がない場合、UTCからオフセットで計算 (簡易版、DST非考慮)
#         print("Warning: pytz not found. Using simple JST offset.")
#         return (datetime.utcnow() + timedelta(hours=9)).date()
#
# --- テスト関数本体 ---

def run_default_prediction_test():
    """
    履歴が1件の場合のデフォルト予測ロジックをテストします。
    """
    print(f"\n--- デフォルト予測ロジックテスト開始 for {user_id_default_test} ---")

    test_utils.create_table_if_not_exists()
    test_utils.clear_table_data(user_id_default_test)

    # 1. 最初の記録のみを投入
    today_date_jst = test_utils.get_current_date_in_jst() 
    first_start = today_date_jst - timedelta(days=20) # 例えば2025-06-16
    first_end = first_start + timedelta(days=DEFAULT_PERIOD_LENGTH - 1) # 例えば2025-06-20 (期間5日)
    
    event = {
        'user_id': user_id_default_test,
        'start_date': first_start.strftime('%Y-%m-%d'),
        'end_date': first_end.strftime('%Y-%m-%d')
    }
    context = {}

    response = put_record.lambda_handler(event, context)
    assert response['statusCode'] == 200, f"最初の記録の追加に失敗: {response}"
    response_body = json.loads(response['body'])
    first_record_id = response_body['record_id']
    print(f"最初の記録投入 ({first_record_id}): {first_start.strftime('%Y-%m-%d')} - {first_end.strftime('%Y-%m-%d')}")

    # レスポンスの検証 (履歴が1件なので、デフォルト周期が使われるはず)
    assert response_body['averageCycle'] == DEFAULT_CYCLE_LENGTH, \
        f"平均周期がデフォルトと一致しません。期待値: {DEFAULT_CYCLE_LENGTH}, 実際: {response_body['averageCycle']}"
    assert response_body['historyCount'] == 1, \
        f"履歴カウントが期待値と異なります。期待値: 1, 実際: {response_body['historyCount']}"

    # 期待される予測開始日: 最新の開始日 (first_start) + デフォルト周期
    expected_predicted_start_date = first_start + timedelta(days=DEFAULT_CYCLE_LENGTH) # 2025-06-16 + 30日 = 2025-07-16
    expected_predicted_end_date = expected_predicted_start_date + timedelta(days=DEFAULT_PERIOD_LENGTH - 1) # 2025-07-16 + 4日 = 2025-07-20

    assert response_body['predictedStartDate'] == expected_predicted_start_date.strftime('%Y-%m-%d'), \
        f"予測開始日が一致しません。期待値: {expected_predicted_start_date.strftime('%Y-%m-%d')}, 実際: {response_body['predictedStartDate']}"
    assert response_body['predictedEndDate'] == expected_predicted_end_date.strftime('%Y-%m-%d'), \
        f"予測終了日が一致しません。期待値: {expected_predicted_end_date.strftime('%Y-%m-%d')}, 実際: {response_body['predictedEndDate']}"

    # DB上のレコードも検証
    retrieved_record = test_utils.get_record_by_id(user_id_default_test, first_record_id)
    assert retrieved_record['prediction_next_start_date'] == expected_predicted_start_date.strftime('%Y-%m-%d')
    assert retrieved_record['prediction_end_date'] == expected_predicted_end_date.strftime('%Y-%m-%d')

    print("✅ 履歴1件の場合のデフォルト予測ロジック検証成功。")
    print(f"--- デフォルト予測ロジックテスト完了 for {user_id_default_test} ---")

    test_utils.clear_table_data(user_id_default_test)


def setup_test_data(user_id):
    """
    複数記録のテスト用に生理記録データをDynamoDBに投入します。
    投入された最新レコードの情報を返します。
    """
    print("--- テストデータセットアップ開始 ---")
    test_utils.clear_table_data(user_id)

    today_date_jst = test_utils.get_current_date_in_jst() 

    # 1. 最初の記録 (最も古い)
    first_start = today_date_jst - timedelta(days=TEST_CYCLE_LENGTH_1 + TEST_CYCLE_LENGTH_2 + 30) # 例: 2025-04-07
    first_end = first_start + timedelta(days=TEST_PERIOD_LENGTH - 1) # 例: 2025-04-13
    
    event1 = {
        'user_id': user_id,
        'start_date': first_start.strftime('%Y-%m-%d'),
        'end_date': first_end.strftime('%Y-%m-%d')
    }
    response1 = put_record.lambda_handler(event1, {})
    response_body1 = json.loads(response1['body'])
    record1_id = response_body1['record_id']
    print(f"テストデータ1投入 ({record1_id}): {first_start.strftime('%Y-%m-%d')} - {first_end.strftime('%Y-%m-%d')}")

    # 2. 2番目の記録
    second_start = first_start + timedelta(days=TEST_CYCLE_LENGTH_1) # 例: 2025-05-05
    second_end = second_start + timedelta(days=TEST_PERIOD_LENGTH - 1) # 例: 2025-05-11
    event2 = {
        'user_id': user_id,
        'start_date': second_start.strftime('%Y-%m-%d'),
        'end_date': second_end.strftime('%Y-%m-%d')
    }
    response2 = put_record.lambda_handler(event2, {})
    response_body2 = json.loads(response2['body'])
    record2_id = response_body2['record_id']
    print(f"テストデータ2投入 ({record2_id}): {second_start.strftime('%Y-%m-%d')} - {second_end.strftime('%Y-%m-%d')}")

    # 3. 最新の記録 (このレコードに予測値が書き込まれることを検証)
    latest_start = second_start + timedelta(days=TEST_CYCLE_LENGTH_2) # 例: 2025-06-06
    latest_end = latest_start + timedelta(days=TEST_PERIOD_LENGTH - 1) # 例: 2025-06-12
    event3 = {
        'user_id': user_id,
        'start_date': latest_start.strftime('%Y-%m-%d'),
        'end_date': latest_end.strftime('%Y-%m-%d')
    }
    response3 = put_record.lambda_handler(event3, {})
    response_body3 = json.loads(response3['body'])
    latest_record_id_from_response = response_body3['record_id']
    print(f"テストデータ3 (最新) 投入 ({latest_record_id_from_response}): {latest_start.strftime('%Y-%m-%d')} - {latest_end.strftime('%Y-%m-%d')}")
    print("--- テストデータセットアップ完了 ---")

    # 予測計算の基準となる情報と、今回投入された最新のレコードIDを返します
    return latest_start, latest_end, today_date_jst, latest_record_id_from_response


def run_combined_test():
    """
    put_record.py の lambda_handler をテストします。
    記録の保存と、複数記録に基づく予測結果の検証を行います。
    """
    print(f"\n--- 複数記録の結合テスト開始 for {user_id_combined_test} ---")

    test_utils.create_table_if_not_exists()

    # 2. テストデータの準備 (3件の記録を投入)
    latest_start_date_from_setup, latest_end_date_from_setup, today_date_jst, latest_record_id_for_setup = setup_test_data(user_id_combined_test)

    # 予測が書き込まれた最新のレコードをDBから取得し、検証
    truly_latest_record_from_db = test_utils.get_record_by_id(user_id_combined_test, latest_record_id_for_setup)

    assert truly_latest_record_from_db is not None, "テストデータがDBに正しく投入されていません。"
    assert truly_latest_record_from_db['start_date'] == latest_start_date_from_setup.strftime('%Y-%m-%d'), \
        "DBから取得した最新レコードの開始日が期待と異なります。"

    # 期待される平均周期の計算 (setup_test_dataで投入された3つのレコードに基づく)
    # 最初の28日と次の32日の周期から平均を計算: (28 + 32) // 2 = 30日
    expected_average_cycle = (TEST_CYCLE_LENGTH_1 + TEST_CYCLE_LENGTH_2) // 2 

    # 期待される予測開始日: 最新の開始日 + 平均周期
    expected_predicted_start_date = latest_start_date_from_setup + timedelta(days=expected_average_cycle) # 2025-06-06 + 30日 = 2025-07-06

    # 期待される予測終了日: 予測開始日 + (最新の生理期間の長さ - 1)
    expected_period_length = (latest_end_date_from_setup - latest_start_date_from_setup).days + 1
    expected_predicted_end_date = expected_predicted_start_date + timedelta(days=expected_period_length - 1)

    print(f"\n--- 予測が書き込まれた最新レコード ({truly_latest_record_from_db['id']}) の検証 ---")
    
    assert 'prediction_next_start_date' in truly_latest_record_from_db, "予測開始日がレコードに含まれていません。"
    assert 'prediction_end_date' in truly_latest_record_from_db, "予測終了日がレコードに含まれていません。"

    assert truly_latest_record_from_db['prediction_next_start_date'] == expected_predicted_start_date.strftime('%Y-%m-%d'), \
        f"予測開始日が一致しません。期待値: {expected_predicted_start_date.strftime('%Y-%m-%d')}, 実際: {truly_latest_record_from_db['prediction_next_start_date']}"
    
    assert truly_latest_record_from_db['prediction_end_date'] == expected_predicted_end_date.strftime('%Y-%m-%d'), \
        f"予測終了日が一致しません。期待値: {expected_predicted_end_date.strftime('%Y-%m-%d')}, 実際: {truly_latest_record_from_db['prediction_end_date']}"

    all_records_after_setup = test_utils.get_all_records(user_id_combined_test)
    assert len(all_records_after_setup) == 3, f"履歴カウントが期待値と異なります。期待値: 3, 実際: {len(all_records_after_setup)}"
    print("✅ 予測値の検証成功 (setup_test_data後のDB状態)。")

    print("\n--- 新規記録の追加とレスポンスの予測結果の検証 ---")
    # さらに新しい記録を追加し、そのレスポンスとDBの更新を検証
    new_record_start = today_date_jst # 例: 2025-07-06
    new_record_end = today_date_jst + timedelta(days=TEST_PERIOD_LENGTH - 1) # 例: 2025-07-12
    
    event = {
        'user_id': user_id_combined_test,
        'start_date': new_record_start.strftime('%Y-%m-%d'),
        'end_date': new_record_end.strftime('%Y-%m-%d')
    }
    context = {}

    response = put_record.lambda_handler(event, context)
    assert response['statusCode'] == 200, f"新規記録の追加と予測に失敗: {response}"
    response_body = json.loads(response['body'])
    print(f"新規記録追加のレスポンス: {response_body}")

    new_record_id = response_body['record_id']
    assert new_record_id is not None, "新規記録のIDがレスポンスに含まれていません。"
    assert response_body['message'] == '記録を保存しました', "メッセージが一致しません。"

    # 新規追加後の期待される平均周期を再計算
    # 履歴: 28日、32日、そして今回追加される新しい周期の長さ
    latest_to_new_cycle_length = (new_record_start - latest_start_date_from_setup).days # (2025-07-06 - 2025-06-06).days = 30日

    # 4つの生理記録（3つの周期）に基づく平均周期
    expected_average_cycle_after_new_record = (TEST_CYCLE_LENGTH_1 + TEST_CYCLE_LENGTH_2 + latest_to_new_cycle_length) // 3 # (28 + 32 + 30) // 3 = 30
    
    expected_predicted_start_date_after_new_record = new_record_start + timedelta(days=expected_average_cycle_after_new_record) # 2025-07-06 + 30日 = 2025-08-05
    expected_predicted_end_date_after_new_record = expected_predicted_start_date_after_new_record + timedelta(days=TEST_PERIOD_LENGTH - 1) # 2025-08-05 + 6日 = 2025-08-11

    assert response_body['averageCycle'] == expected_average_cycle_after_new_record, \
        f"新規追加後の平均周期が一致しません。期待値: {expected_average_cycle_after_new_record}, 実際: {response_body['averageCycle']}"
    assert response_body['historyCount'] == 4, \
        f"新規追加後の履歴カウントが一致しません。期待値: 4, 実際: {response_body['historyCount']}"
    assert response_body['predictedStartDate'] == expected_predicted_start_date_after_new_record.strftime('%Y-%m-%d'), \
        f"新規追加後の予測開始日が一致しません。期待値: {expected_predicted_start_date_after_new_record.strftime('%Y-%m-%d')}, 実際: {response_body['predictedStartDate']}"
    assert response_body['predictedEndDate'] == expected_predicted_end_date_after_new_record.strftime('%Y-%m-%d'), \
        f"新規追加後の予測終了日が一致しません。期待値: {expected_predicted_end_date_after_new_record.strftime('%Y-%m-%d')}, 実際: {response_body['predictedEndDate']}"

    print("✅ 新規記録追加後のレスポンス予測検証成功。")

    # 新しく追加されたレコードが最新となり、そのレコードに予測情報が書き込まれているかDBから確認
    print(f"\n--- DB上の新規追加後の最新レコード ({new_record_id}) の検証 ---")
    latest_retrieved_record_after_new = test_utils.get_record_by_id(user_id_combined_test, new_record_id)
    
    assert latest_retrieved_record_after_new is not None, "新規追加後の最新の記録がDBから取得できませんでした。"
    assert latest_retrieved_record_after_new['prediction_next_start_date'] == expected_predicted_start_date_after_new_record.strftime('%Y-%m-%d'), \
        f"DB上の予測開始日が一致しません。期待値: {expected_predicted_start_date_after_new_record.strftime('%Y-%m-%d')}, 実際: {latest_retrieved_record_after_new['prediction_next_start_date']}"
    assert latest_retrieved_record_after_new['prediction_end_date'] == expected_predicted_end_date_after_new_record.strftime('%Y-%m-%d'), \
        f"DB上の予測終了日が一致しません。期待値: {expected_predicted_end_date_after_new_record.strftime('%Y-%m-%d')}, 実際: {latest_retrieved_record_after_new['prediction_end_date']}"
    
    print("✅ 新規記録追加後のDB予測検証成功。")

    print("\n--- 複数記録の結合テスト完了 ---")

if __name__ == '__main__':
    try:
        run_default_prediction_test() # 履歴が1件の場合のテストを実行
        run_combined_test() # 履歴が複数ある場合のテストを実行
    finally:
        # テスト終了後にデータをクリーンアップ
        test_utils.clear_table_data(user_id_default_test)
        test_utils.clear_table_data(user_id_combined_test)