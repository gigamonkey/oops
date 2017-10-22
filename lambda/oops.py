#
# Lambda functions for the Oops bot.
#

import json

def oops(event, context):

    body = event

    if 'challenge' in body:
        return body['challenge']
    else:
        return 'hello'
