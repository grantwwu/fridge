# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import post, get

baseURL = 'http://grantwu.me:5000/'

def _url(suffix):
    return baseURL + suffix

def item2text(item):
    text = item['amount'] + ' '
    if item['unit'] != 'Count':
        text += item['unit']
        # Pluralize unit
        if item['amount'] > 0:
            text += 's'
        text += ' of '
        text += item['label']
    else:
        if item['amount'] > 0:
            text += pluralize(item['label'])
        else:
            text += item['label']
    return text

def get_items():
    items = get(_url('items')).json()
    if length(items) == 0:
        return tellResponse('Your Fridge is empty!')
    else:
        text = 'You have '
        text += ', '.join(item2text(i) for i in items[0:length(items)-1])
        if length(items) > 1:
            text += ' and ' + item2text(i)
        return tellResponse(text)


def handler(event, context):
    request = event['request']
    if request['type'] == 'LaunchRequest':
        pass
        # Go to help stuff
    elif request['type'] == 'SessionEndedRequest':
        pass
    elif request['type'] == 'IntentRequest':
        intent = request['intent']

        if intent['name'] == 'GetItemIntent':
            return get_items()
        elif intent['name'] == 'AddItemIntent':
            pass
        elif intent['name'] == 'FindItemIntent':
            pass
        elif intent['name'] == 'RemoveItemIntent':
            pass
        elif intent['name'] == 'UpdateItemIntent':
            pass
        elif intent['name'] == 'DeleteItemIntent':
            pass
        elif intent['name'] == 'CheckExpirationFutureIntent':
            pass
        elif intent['name'] == 'CheckExpirationIntent':
            pass
        elif intent['name'] == 'CheckRunningLowIntent':
            pass
        elif intent['name'] == 'MakeRecipeIntent':
            pass
        elif intent['name'] == 'HelpIntent':
            pass
        else:
            pass
    else:
        pass

def tellResponse(text):
    responseDict = { 'version' : '1.0',
                     'sessionAttributes' : {},
                     'response' : {
                         'outputSpeech' : {
                             'type' : 'PlainText',
                             'text' : text
                         }
                     },
                     'shouldEndSession' : True
                   }
    return responseDict

# GetItemsIntent

# Alexa, ask fridge helper what I have
#   You have ...


# AddItemIntent

# Alexa, tell fridge helper to add {number} {unit} of {item}
#   Taking picture...
#   Added <number> <unit> <item>

# Alexa, tell fridge helper to add {number} {item}
#   Taking picture...
#   Added <number> <item>

# Alexa, tell fridge helper to add some {item}
#   Taking picture and weighing item...
#   Added <weight> of <item>.


# RemoveItemIntent

# Alexa, tell fridge helper to remove {number} {units} of {item}
#   Removed <number> <units> of <item>

# Alexa, tell fridge helper to remove {number} {item}
#   Removed <number> <item>


# UpdateItemIntent

# Alexa, tell fridge helper I now have {number} {units} of {item}
#   Quantity of <item> updated to <number> <units>

# Alexa, tell fridge helper I now have {number} {item}
#   Quantity of <item> updated to <number>

# Alexa, ask fridge helper to update how much {item} I have
#   Updated weight of <item> to <number> kilograms


# DeleteItemIntent

# Alexa, tell fridge helper I'm out of {item}


# CheckExpirationFutureIntent

# Alexa, ask fridge helper what expires within the next {duration}
#   ... is expired.
#   ... will expire in <duration>.
#   etc.

# Alexa, ask fridge helper what expires soon (see above, with timespan of 1 week)


# CheckExpirationIntent

# Alexa, ask fridge helper what's expired (see above, with timespan of 0)


# CheckRunningLowIntent

# Alexa, ask fridge helper what I'm running out of.
#   You only have <>...


# Alexa, ask fridge helper can I make {recipe}?
#   You have everything you need to make <recipe>
#   OR
#   You are missing ...
