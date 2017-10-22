#
# Lambda functions for the Oops bot.
#

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
    print("message_received invoked")
    time.sleep(10)
    print("Done sleeping")
    print(json.dumps(event))
