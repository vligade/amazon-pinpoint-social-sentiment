import base64
import json
import boto3
import uuid
import datetime
import os

client = boto3.client('comprehend')
pinpointclient = boto3.client('pinpoint')
print('Loading function')

def lambda_handler(event, context):
    app_id = os.environ['app_id']
    
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print(payload)
        screen_name = json.loads(payload)['user']['screen_name']
        
        try: 
            pinpointclient.get_endpoint(ApplicationId=app_id, EndpointId=screen_name)
        except Exception as e:
            print("Error occurred: ", e)
        else:
            # if endpoint exists, do sentiment analysis, send push, update endpoint
            response = client.detect_sentiment(
                Text=json.loads(payload)['text'],
                LanguageCode='en'
            )
            print(response)
            
            if response['Sentiment'] == 'POSITIVE':
                pinpointresponse = pinpointclient.send_users_messages(
                    ApplicationId=app_id,
                    SendUsersMessageRequest={
                        'Users': {
                            screen_name: {}
                        },
                        'MessageConfiguration': {
                            'APNSMessage': {
                                'Action': 'OPEN_APP',
                                'Body': 'Thanks for the feedback! Fill out this 2-question survey and get free gear https://tinyurl.com/SomeSurveyURL',
                                'Title': 'Thank you very much!'
                            }
                        }
                    }
                )
                print(pinpointresponse)
                endpointresponse = pinpointclient.update_endpoint(
                    ApplicationId=app_id,
                    EndpointId=screen_name,
                    EndpointRequest={
                        'EffectiveDate': datetime.datetime.now().isoformat(),
                        'RequestId': str(uuid.uuid4()),
                        'User': {
                            'UserAttributes': {
                                'Sentiment': [
                                    'Positive',
                                ]
                            }
                        }
                    }
                )
                print(endpointresponse)
            
    return 'Successfully processed {} records.'.format(len(event['Records']))
