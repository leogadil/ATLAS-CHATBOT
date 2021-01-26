
import random
import json
import os.path

class menu:

    def get_menu():
        with open('./Menu/menu.json') as f:
            menu = json.load(f)
        return menu

    @staticmethod
    def run(data):
        menu_ = menu.get_menu()['menu']
        reply = ""
        reply += "$MENUINTRO$\n"
        reply += "\tOrder Name\t\tPrice\n\t-----------------------------"
        for product in menu_:
            if len(product['Order_name']) <= 7:
                reply += "\n\t{}\t\t\t {}".format(product['Order_name'], product['Order_price'])
            else:
                reply += "\n\t{}\t\t {}".format(product['Order_name'], product['Order_price'])
        if reply != "":
            data['output']['reply_template'] = reply
        else:
            data['output']['reply_template'] = "$EMPTY$"
        data['output']['stopatpunct'] = False
        data['output']['fast'] = True
        return data