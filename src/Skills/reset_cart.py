
class reset():

    def run(data):
        reply = ""
        data['user'].Delete_Orders()
        reply = "$DELETED$"
        data['output']['reply_template'] = reply
        return data