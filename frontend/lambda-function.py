import json
import boto3
import logging
from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vote-table')  

def lambda_handler(event, context):
    try:
        
        logger.info(f"Received event: {json.dumps(event)}")
        
        
        body = json.loads(event.get('body', '{}'))
        choice = body.get('choice', 'unknown')
        
        
        logger.info(f"VOTE_RECEIVED: User voted for '{choice}' at {datetime.utcnow().isoformat()}")
        
       
        response = table.put_item(
            Item={
                'Choice': choice,
                'Timestamp': datetime.utcnow().isoformat(),
                'RequestId': context.aws_request_id
            }
        )
        
        
        logger.info(f"VOTE_STORED: Successfully stored vote for '{choice}' in DynamoDB")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'message': f'Vote for {choice} recorded',
                'vote': choice,
                'timestamp': datetime.utcnow().isoformat()
            })
        }
        
    except Exception as e:
        
        logger.error(f"ERROR_PROCESSING_VOTE: {str(e)}")
        logger.error(f"Event that caused error: {json.dumps(event)}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'error': 'Failed to process vote',
                'message': str(e)
            })
        }
