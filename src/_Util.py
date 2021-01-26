from os import system, name
import re
import json
import random

class Util:
    @staticmethod
    def Clear(): 
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear')

    @staticmethod
    def ReplaceTags(str):
        with open('src\\response.json', encoding="utf-8") as RT:
            response_template = json.load(RT)
            if str is not None:
                for word in str.split():
                    word = re.sub(r'\!|\,|\.|\?|\:', '', word)
                    try:
                        random_response = random.choice(response_template[word])
                        str = str.replace(word, random_response)
                    except:
                        pass
        return str

    @staticmethod
    def ReplaceVars(str):
        with open('src\\Options.json', encoding="utf-8") as RT:
            response_template = json.load(RT)
            if str is not None:
                for word in str.split():
                    word = re.sub(r'\!|\,|\.|\?|\:|\n', '', word)
                    try:
                        variable = response_template[word]
                        str = str.replace(word, variable)
                    except:
                        pass
        return str