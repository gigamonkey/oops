#
# Lambda functions for the Oops bot.
#

import json

def oops(event, context):
    body = json.loads(event['body'])

    if 'challenge' in body:
        return respond(body['challenge'])
    else:
        return respond('hello')

def respond(body):
    return {
        "statusCode": 200,
        "headers": {},
        "body": body
    }
