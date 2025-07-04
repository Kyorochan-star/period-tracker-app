import boto3
from datetime import datetime, timedelta

#sns = boto3.client('sns')
# 実際のSNSは使えないため、printで代用
def send_period_prediction(event, context):
    from datetime import datetime, timedelta

    user_id = event['userId']
    last_record = event['recordDate']
    next_period = datetime.strptime(last_record, "%Y-%m-%d") + timedelta(days=28)

    message = f'{user_id}さん、次の予定は{next_period.strftime("%Y-%m-%d")}です'
    print(f"[Mock SNS] Subject: 次回周期の予測\nMessage: {message}")

#AWS SNSに送信する用
# def send_period_prediction(event, context):
#     user_id = event['userId']
#     last_record = event['recordDate']
#     next_period = datetime.strptime(last_record, "%Y-%m-%d") + timedelta(days=28)

#     sns.publish(
#         TopicArn='arn:aws:sns:ap-northeast-1:xxxxxx:PeriodNotify',
#         Message=f'{user_id}さん、次の予定は{next_period.strftime("%Y-%m-%d")}です',
#         Subject='次回周期の予測'
#     )
