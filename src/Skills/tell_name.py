
class name():

    def run(data):
        reply = ""
        name = ""

        name_continuation = 0
        if len(data['input']['entities']) > 0:
            for w in data['input']['entities']:
                if w[1] == "PERSON": 
                    name_continuation += 1
                    name += w[0]
        if name_continuation <= 0: 
            reply += "$EMPTY$."
            data['output']['reply_template'] = reply
            return data 

        rename = data['user'].set_Name(name)

        if rename:
            reply += "$GREET2NAME$, {}.".format(name)
        else:
            reply += "$EMPTY$."
        if reply != "":
            data['output']['reply_template'] = reply
        else:
            data['output']['reply_template'] = "$EMPTY$"
        return data