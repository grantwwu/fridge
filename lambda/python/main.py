# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random

from requests import post, get, delete

import Recipe

baseURL = 'http://grantwu.me:5000/'

def _url(suffix):
    return baseURL + suffix

# It only supports one format and doesn't pad input to mm/dd/yyyy.
# This works because we only support times after the 10th of December of 2015
# and before the 31st.
# It's called shitty_stftime for a reason!!!  I was *extremely* lazy.
def shitty_strftime(month, day, year):
    return str(month) + '/' + str(day) + '/' + str(year)

def canonicalize_unit(item):
    if not item:
        return None
    else:
        if item[0] == 'l' or item[0] == 'L':
            return 'Liter'
        elif item[0] == 'k' or item[0] == 'K':
            return 'Kilogram'
        elif item[0] == 'c' or item[0] == 'C':
            return 'Count'
        else:
            return None

def item2text(item):
    text = str(item['amount']) + ' '
    if item['unit'] != 'Count':
        text += item['unit']
        # Pluralize unit
        if item['amount'] > 1:
            text += 's'
        text += ' of '
        text += item['label']
    else:
        if item['amount'] > 1:
            # Shitty pluralization
            text += item['label'] + 's'
        else:
            text += item['label']
    return text

# Alexa, ask fridge helper what I have
#   You have ...
def get_items():
    items = get(_url('items')).json()
    if len(items) == 0:
        return tellResponse('Your Fridge is empty!')
    elif len(items) == 1:
        text = 'You have ' + item2text(items[0])
    else:
        text = 'You have '
        text += ', '.join(item2text(i) for i in items[0:len(items)-1])
        text += ' and ' + item2text(items[len(items)-1])
    return tellResponse(text)

# Alexa, tell fridge helper to add {number} {unit} of {item}
#   Taking picture...
#   Added <number> <unit> <item>

# Alexa, tell fridge helper to add {number} {item}
#   Taking picture...
#   Added <number> <item>

# Alexa, tell fridge helper to add some {item}
#   Taking picture and weighing item...
#   Added <weight> of <item>.
# TODO: Make this actually take an expiration
def add_item(number, unit, item):
    if not number and not unit and item:
        weight_response = get(_url('weigh')).json()
        number = float(weight_response['weight'])
        unit = 'Kilogram'
    elif not unit and number and item:
        unit = 'Count'
    elif number and unit and item:
        pass
    else:
        # Lol error handling
        return None

    unit = canonicalize_unit(unit)

    picture_response = post(_url('take_picture')).json()
    picture_id = int(picture_response['picture_id'])

    year = 2015
    month = 12
    day = random.randint(13, 31)

    # Whoops, I haven't been super consistent in my naming...
    form = { 'label' : item,
             'amount' : number,
             'unit' : unit,
             'expdate' : shitty_strftime(month, day, year),
             'picture_id' : picture_id }

    post(_url('add'), data=form)

    text = 'Added ' + item2text({'label' : item, 'amount' : number, 'unit' : unit})
    return tellResponse(text)

# FindItemIntent

def find_item(item):
    items = get(_url('items')).json()
    for i in items:
        if item and i['label'].lower() == item.lower():
            text = 'You have ' + item2text(i)
            return tellResponse(text)

    return tellResponse('Sorry, fridge helper was unable to find that.')

# DeleteItemIntent

# Alexa, tell fridge helper I'm out of {item}

def delete_item(item):
    id = None
    items = get(_url('items')).json()
    for i in items:
        if item and i['label'].lower() == item.lower():
            id = i['id']
            delete(_url('items/' + str(id)))
            text = 'Deleted ' + item2text(i)
            return tellResponse(text)

    return tellResponse('Sorry, fridge helper was unable to find that.')

# UpdateItemIntent

# Alexa, tell fridge helper I now have {number} {units} of {item}
#   Quantity of <item> updated to <number> <units>

# Alexa, tell fridge helper I now have {number} {item}
#   Quantity of <item> updated to <number>

# Alexa, ask fridge helper to update how much {item} I have
#   Updated weight of <item> to <number> kilograms

def update_item(number, unit, item):
    id = None
    items = get(_url('items')).json()
    for i in items:
        if item and i['label'].lower() == item.lower():
            id = i['id']
            if number and unit:
               number = float(number)
               unit = canonicalize_unit(unit)
            elif number and not unit:
                number = float(number)
                unit = 'Count'
            elif not number and not unit:
                weight_response = get(_url('weigh')).json()
                number = float(weight_response['weight'])
                unit = 'Kilogram'
            else:
                return None
            form = { 'amount' : number,
                     'unit' : unit }
            post(_url('items/' + str(id)), data=form)
            i['amount'] = number
            i['unit'] = unit
            text = 'Updated:  ' + item2text(i)
            return tellResponse(text)

def expires_week(i):
    expday = int(i['expiration']['day'])
    expmonth = int(i['expiration']['day'])
    return expmonth <= 12 or expday <= 9 # Yes, I hard coded the presentation date.

def check_expiration_future():
    items = get(_url('items')).json()
    items = [i for i in items if expires_week(i)]

    if len(items) == 0:
        return tellResponse('Nothing expires in your fridge within a week.')
    elif len(items) == 1:
        text = item2text(items[0]) + ' is expiring within a week'
    else:
        text = ', '.join(item2text(i) for i in items[0:len(items)-1])
        text += ' and ' + item2text(items[len(items)-1])
        text += ' are expiring within a week'
    return tellResponse(text)

def expired(i):
    expday = int(i['expiration']['day'])
    expmonth = int(i['expiration']['day'])
    return expmonth <= 12 or expday <= 22# Yes, I hard coded the presentation date.

def check_expiration():
    items = get(_url('items')).json()
    items = [i for i in items if expired(i)]

    if len(items) == 0:
        return tellResponse('Nothing is expired in your fridge.')
    elif len(items) == 1:
        text = item2text(items[0]) + ' is expired'
    else:
        text = ', '.join(item2text(i) for i in items[0:len(items)-1])
        text += ' and ' + item2text(items[len(items)-1])
        text += ' are expired'
    return tellResponse(text)

def check_running_low():
    items = get(_url('items')).json()
    eggs = [i for i in items if i['label'.lower()] == 'eggs']
    if len(eggs) > 0:
        eggs = eggs[0]
    else:
        eggs = { 'amount' : 0 }
    milk = [i for i in items if i['label'.lower()] == 'milk']
    if len(milk) > 0:
        milk = milk[0]
    else:
        milk = { 'amount' : 0 }
    eggs_low = eggs['amount'] < 6
    milk_low = milk['amount'] < 1
    text = ''
    if not eggs_low and not milk_low:
        text = 'You have your staple ingredients!'
    elif eggs_low and milk_low:
        text = 'You need both eggs and milk!'
    else:
        if eggs_low:
            text = 'You need eggs!'
        else:
            text = 'You need milk!'

    return tellResponse(text)

def make_recipe(recipe):
    items = get(_url('items')).json()
    items = [i['label'].lower() for i in items]

    recipe_request = Recipe.Recipe()
    ingredients = recipe_request.gen_search_title_request(recipe.replace(' ', '%20'))
    ingredients_have = [i for i in ingredients if i in items]
    ingredients_missing = [i for i in ingredients if i not in items]
    text = ''
    if len(ingredients_have) == len(ingredients):
        text = 'You have everything you need!'
    else:
        text = ''
        if len(ingredients_have) == 1:
            text += 'You have' + ingredients_have[0]
        elif len(ingredients_have) >= 1:
            text += 'You have '
            text += ', '.join(ingredients_have[0:len(ingredients_have)-1])
            text += ' and ' + ingredients_have[len(ingredients_have)-1]

        text += '\n'

        if len(ingredients_need) == 1:
            text += 'You need' + ingredients_need[0]
        elif len(ingredients_need) >= 1:
            text += 'You need '
            text += ', '.join(ingredients_need[0:len(ingredients_need)-1])
            text += ' and ' + ingredients_need[len(ingredients_need)-1]

def handler(event, context):
    request = event['request']
    if request['type'] == 'LaunchRequest':
        print 'Getting LaunchRequest'
        # Go to help stuff
    elif request['type'] == 'SessionEndedRequest':
        print 'Getting SessionEndedRequest'
    elif request['type'] == 'IntentRequest':
        intent = request['intent']

        if intent['name'] == 'GetItemsIntent':
            return get_items()
        elif intent['name'] == 'AddItemIntent':
            number = intent['slots']['Number'].get('value')
            unit = intent['slots']['Unit'].get('value')
            item = intent['slots']['Item'].get('value')
            return add_item(number, unit, item)
        elif intent['name'] == 'FindItemIntent':
            item = intent['slots']['Item'].get('value')
            return find_item(item)
        elif intent['name'] == 'DeleteItemIntent':
            item = intent['slots']['Item'].get('value')
            return delete_item(item)
        elif intent['name'] == 'UpdateItemIntent':
            number = intent['slots']['Number'].get('value')
            unit = intent['slots']['Unit'].get('value')
            item = intent['slots']['Item'].get('value')
            return update_item(number, unit, item)
        elif intent['name'] == 'CheckExpirationFutureIntent':
            return check_expiration_future()
        elif intent['name'] == 'CheckExpirationIntent':
            return check_expiration()
        elif intent['name'] == 'CheckRunningLowIntent':
            return check_running_low()
        elif intent['name'] == 'MakeRecipeIntent':
            return make_recipe(recipe)
        elif intent['name'] == 'HelpIntent':
            pass
        else:
            print 'Intent: ' + intent['name']
            pass
    else:
        print request['type']
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

# CheckRunningLowIntent

# Alexa, ask fridge helper what I'm running out of.
#   You only have <>...

# Alexa, ask fridge helper can I make {recipe}?
#   You have everything you need to make <recipe>
#   OR
#   You are missing ...
