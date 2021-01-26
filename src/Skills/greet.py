
import random

class greet:

    @staticmethod
    def run(data):
        reply = ""
        reply += "$HELLOBACK$"
        chance = random.random()
        if chance > 0.6:
            reply += ", $ASKGENERAL$"
        else:
            reply += "."

        data['output']['reply_template'] = reply
        return data