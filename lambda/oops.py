#
# Lambda functions for the Oops bot.
#

from urllib.parse import urlencode
from urllib.request import urlopen, Request
import boto3
import json
import time

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
        if text_contains(e['text'], 'down!'):
            set_topic("Incident open! Alerted by <@{}>!".format(e['user']), e['channel'])
        else:
            post_message('Hello <@{}>'.format(e['user']), e['channel'])
    else:
        print("Ignoring")


def text_mentions(text, user):
    return text_contains(text, '<@{}>'.format(user))


def text_contains(text, sub):
    return text.find(sub) > -1


def post_message(text, channel):
    return slack('chat.postMessage', {'text': text, 'channel': channel})


def set_topic(topic, channel):
    return slack('channels.setTopic', {'topic': topic, 'channel': channel})


def users_info(id):
    return slack('users.info', {'user': me})


def slack(method, args):
    url = 'https://slack.com/api/' + method
    args['token'] = config['oauth-token']
    data = urlencode(args).encode('utf-8')
    print('Invoking Slack API: {}'.format(method))
    with urlopen(Request(url, data = data, method = 'POST')) as f:
        text = f.read().decode('utf-8')
        print(text)
        return json.loads(text) if f.getcode() == 200 else None
