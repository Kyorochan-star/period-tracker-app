import predict
import json

# テストユーザーID
user_id = 'testuser001'

event = {
    'requestContext': {
        'authorizer': {
            'claims': {
                'sub': user_id
            }
        }
    }
}
context = {}

print(f"\n--- Predicting next period for {user_id} ---")
response = predict.lambda_handler(event, context)
prediction_result = json.loads(response['body'])
print(f"Prediction Result: {prediction_result}")