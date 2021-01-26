
import random
import json
import sys, traceback
from src.Skills.see_menu import menu
from fuzzywuzzy import fuzz

class remove_order:

    # im lazy and out of ideas so stackoverflow guy hook me up
    # Author: https://stackoverflow.com/users/6636836/andrew
    def text2int (textnum, numwords={}):
        if not numwords:
            units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):  numwords[word] = (1, idx)
            for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

        ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
        ordinal_endings = [('ieth', 'y'), ('th', '')]

        textnum = textnum.replace('-', ' ')

        current = result = 0
        curstring = ""
        onnumber = False
        for word in textnum.split():
            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)

                if word not in numwords:
                    if onnumber:
                        curstring += repr(result + current) + " "
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = numwords[word]

                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True

        if onnumber:
            curstring += repr(result + current)

        return curstring

    def clean_order(order):
        cleaned_order = []
        for x in range(len(order)):
            o1 = order[x]
            if x+1 < len(order):
                o2 = order[x+1]
            else:
                o2 = None

            if o1[1] == "ORDER_COUNT":
                if o2 is not None and o2[1] == "ORDER":
                    cleaned_order.append({
                        "name": o2[0],
                        "count": o1[0],
                        "database_approximate": None
                    })
            elif o1[1] == "ORDER" and order[x-1][1] != "ORDER_COUNT":
                cleaned_order.append({
                    "name": o1[0],
                    "count": "one",
                    "database_approximate": None
                })
        # print("clean_order: ", cleaned_order)
        return cleaned_order

    def approximate_order(order):
        menu_ = menu.get_menu()['menu']

        try:
            for order_item in order:
                leaderboard = []
                for db_item in menu_:
                    leaderboard.append((fuzz.ratio(order_item['name'], db_item['Order_name'].lower()), db_item))
                leaderboard.sort(key=lambda x: x[0], reverse=True)

                semifinalsleaderboard = []

                for nominies in leaderboard:
                    if nominies[0] > 60:
                        semifinalsleaderboard.append(nominies)

                if len(semifinalsleaderboard) > 0:
                    order_item['database_approximate'] = semifinalsleaderboard[0][1]
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)
        return order

    @staticmethod
    def run(data):
        reply = ""
        order = []

        order_continuation = 0
        if len(data['input']['entities']) > 0:
            for w in data['input']['entities']:
                if w[1] == "ORDER_COUNT": order_continuation += 1
                if w[1] == "ORDER": order_continuation += 1
        if order_continuation <= 0: 
            return data 


        for key, value in data['input']['entities']:
            order.append([key, value])

        cleaned_order = remove_order.clean_order(order)

        cleaned_order = remove_order.approximate_order(cleaned_order)

        for o in cleaned_order:
            try:
                o['count'] = int(remove_order.text2int(o['count']))
            except ValueError:
                o['count'] = 1

        not_order = []
        for i in range(len(cleaned_order)):
            if cleaned_order[i]['database_approximate'] is None:
                not_order.append(cleaned_order[i])
                del cleaned_order[i]


        # create response 
        if len(cleaned_order) > 1:
            reply += "$PURGEINTRO$ "
            for x in range(len(cleaned_order)):
                if cleaned_order[x]['database_approximate'] is not None:
                    if x <= 0:
                        reply += cleaned_order[x]['database_approximate']['Order_name']
                    else:
                        reply += " and " + cleaned_order[x]['database_approximate']['Order_name']
            reply += " $ORDEROUTRO$"
        elif len(cleaned_order) == 1:
            if cleaned_order[0]['database_approximate'] is not None:
                reply += "$PURGEINTRO$ "
                reply += cleaned_order[0]['database_approximate']['Order_name']
                reply += " $PURGEOUTRO$"
        elif len(cleaned_order) > 0:
            _or = ""
            for x in not_order:
                _or += " " + x['name']
            reply += "I'm sorry, we dont serve" + _or + "."

        # print(cleaned_order)

        data['user'].delete_Item(cleaned_order)
        if reply != "":
            data['output']['reply_template'] = reply
        else:
            data['output']['reply_template'] = "$EMPTY$"
        return data