import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vote-table')  

def lambda_handler(event, context):
    body = json.loads(event['body'])
    choice = body.get('choice', 'unknown')
    
    table.put_item(Item={'Choice': choice})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Vote for {choice} recorded'})
    }
