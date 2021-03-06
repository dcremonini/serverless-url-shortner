import json
import random
import string
import boto3
import os
import time

key_length=10
client = boto3.resource('dynamodb')
table = client.Table(os.getenv('DYNAMODB_TABLE'))

def index(event, context):
    random_key = generate_random_key(key_length)
    reqestData = json.loads(event['body'])
    

    if 'url' not in reqestData:
        return {
            "statusCode": 422,
            "body": json.dumps({
                "message": "url parameter not found."
            }),
        }

    input = {
        'pk': 'short_url#' + random_key,
        'timestamp': int(time.time()),
        'type': 'short-url',
        'resource_value': random_key,
        'link': reqestData['url'],
        'status': True
    }
    result = table.put_item(Item=input)

    output = {
        'url': reqestData['url'],
        'short_code': random_key 
    }

    return {
        "statusCode": 200,
        "body": json.dumps(output),
        "headers": {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*'
        }
    }


def generate_random_key(length):
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(length)])
