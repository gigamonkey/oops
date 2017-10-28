#
# Lambda functions for the Oops bot.
#

from urllib.parse import urlencode
from urllib.request import urlopen, Request
import boto3
import json
import time

slack_url = 'https://slack.com/api/'

with open('config.json') as f:
    config = json.load(f)

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
            FunctionName='event_callback',
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


def event_callback(event, context):
    print("event_callback")
    print(json.dumps(event))

    bot = config['bot_user']
    e = event['event']

    if e['user'] == bot:
        print("Ignoring message from myself.")
        return

    if e['type'] == 'message' and text_mentions(e['text'], bot):
        print('Setting topic.')
        set_topic("Setting the topic from the bot for {}!".format(e['user']), e['channel'])
    else:
        print("Ignoring")


def text_mentions(text, user):
    return text.find('<@{}>'.format(user)) > -1


def send_to_general(text):
    url = config['webhooks']['post_general']
    headers = { 'Content-type': 'application/json; charset=utf-8' }
    data = json.dumps({'text': text}).encode('utf-8')
    with urlopen(Request(url, data = data, headers = headers, method = 'POST')) as f:
        print(f.getcode())


def set_topic(topic, channel):
    url = slack_url + 'channels.setTopic'
    args = {
        'token': config['oauth-token'],
        'topic': topic,
        'channel': channel
    }
    data = urlencode(args).encode('utf-8')

    with urlopen(Request(url, data = data, headers = {}, method = 'POST')) as f:
        print(f.getcode())
        print(f.read().decode('utf-8'))
