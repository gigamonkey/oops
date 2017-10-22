#
# Lambda functions for the Oops bot.
#

from urllib.request import urlopen, Request
import boto3
import json
import time

client = boto3.client('lambda')

def oops(event, context):

    "Main entry point for the OopsBot. Dispatches events asynchronously to another Lambda."

    type = event['type']

    if type == 'url_verification':
        # Slack tests a bot when you register the URL by sending a
        # challenge that you need to echo back.
        return event['challenge']
    elif type == 'event_callback':
        # Otherwise we're actually being invoked. Since we need to
        # return 200 quickly we actually dispatch asynchronously to
        # another Lambda function.
        response = client.invoke(
            FunctionName='message_received',
            InvocationType='Event',
            LogType='None',
            ClientContext='string',
            Payload=json.dumps(event).encode('utf-8')
        )
        # TODO: should really check for response['status'] == 202
        # before we return 200.
        print(response)
        return 'ok'
    else:
        return "Don't know what to do with {}".format(type)


def message_received(event, context):
    print("event_callback")
    print(json.dumps(event))
    if ('bot_id' not in event['event']) or (event['event']['bot_id'] is None):
        send_to_general('Hello from AWS.')


def send_to_general(text):
    url = 'REDACTED'
    headers = { 'Content-type': 'application/json; charset=utf-8' }
    data = json.dumps({'text': text}).encode('utf-8')
    with urlopen(Request(url, data = data, headers = headers, method = 'POST')) as f:
        print(f.getcode())
