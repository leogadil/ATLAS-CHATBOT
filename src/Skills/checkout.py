from src._Order import Order
from src._Util import Util
import time

class checkout():

    def run(data):
        reply = ""

        checkout_ = data['user'].checkout()

        if checkout_ is not None:
            if checkout_ == "CONFIRMED":
                reply = ""
                cart_reciept = data['user'].calculate()
                cart_manifest = data['user'].Orders
                
                reply += Util.ReplaceTags("$CHECKOUTINTRO$").format(duration=cart_reciept['Duration']) + "\n"
                reply += "\tOrders\t\t\tQuantity\tPrice\n\t---------------------------------------------"

                if len(cart_manifest) > 0:
                    for product in cart_manifest.values():
                        if len(product['Order_name']) <= 7:
                            reply += "\n\t{}\t\t\t{}\t\t {}".format(product['Order_name'], product['Order_count'], (product['Order_price'] * product['Order_count']))
                        else:
                            reply += "\n\t{}\t\t{}\t\t {}".format(product['Order_name'], product['Order_count'], (product['Order_price'] * product['Order_count']))
                    reply += "\n\t---------------------------------------------\n\t{}\t\t\t{}\t\t {}".format("Total", cart_reciept['Items'], cart_reciept['Price'])
                    reply += "\n\nAtlas: Thank you {}. Bye".format(data['user'].Name)
                data['user'].ResetAll()
                data['end'] = True
            elif checkout_ == "NAMEEMPTY":
                reply = "$ASKNAME$"
        else:
            reply = "$EMPTYCART$"

        data['output']['reply_template'] = reply
        data['output']['stopatpunct'] = False
        data['output']['fast'] = True

        
        return data