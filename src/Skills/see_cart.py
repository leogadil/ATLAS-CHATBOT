
class cart:

    def run(data):
        reply = ""
        cart_reciept = data['user'].calculate()
        cart_manifest = data['user'].Orders
        
        reply += "$CARTINTRO$\n"
        reply += "\tOrders\t\t\tQuantity\tPrice\n\t---------------------------------------------"

        if len(cart_manifest) > 0:
            for product in cart_manifest.values():
                if len(product['Order_name']) <= 7:
                    reply += "\n\t{}\t\t\t{}\t\t {}".format(product['Order_name'], product['Order_count'], (product['Order_price'] * product['Order_count']))
                else:
                    reply += "\n\t{}\t\t{}\t\t {}".format(product['Order_name'], product['Order_count'], (product['Order_price'] * product['Order_count']))
            reply += "\n\t---------------------------------------------\n\t{}\t\t\t{}\t\t {}".format("Total", cart_reciept['Items'], cart_reciept['Price'])
        else:
            reply += "\n\t                    empty                    "
            reply += "\n\t---------------------------------------------"
        data['output']['reply_template'] = reply
        data['output']['stopatpunct'] = False
        data['output']['fast'] = True
        return data