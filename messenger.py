import time
import random
import string
from src._Util import Util
from src._Chatbot import CHATBOT

Util.Clear()

bot = CHATBOT();

def Type(str, waittime=0.02, newline=True, stopatpunct=False, fast=False):
    time.sleep(1)
    for letter in str:
        print(letter, end = '',flush=True)
        if letter != "-":
            if fast == False:
                time.sleep(random.uniform(0.05, 0.03))
            else:
                time.sleep(random.uniform(0.0, 0.02))
        if letter in string.punctuation and stopatpunct and letter != "'" and letter != "-":
            time.sleep(1)
        

command = ""
while((command != 'exit()')):
    
    command = input("\nYou: ")
    print("\n"+Util.ReplaceVars('Atlas: '), end='')
    bot_reply = bot.GetReply(command)
    bot_stopatpunct = bot_reply['output']['stopatpunct']
    bot_fastType = bot_reply['output']['fast']
    
    # print(bot_reply['output']['reply'])
    Type(bot_reply['output']['reply'] + "\n", stopatpunct=bot_stopatpunct, fast=bot_fastType)
    # print("\n\t\t\t\t\tEntities: ", bot_reply['input']['entities'])
    # print("\t\t\t\t\tIntent: ", bot_reply['input']['intent'])
    # print("\t\t\t\t\tQuery: ", bot_reply['input']['query'])
    if bot_reply['end'] == True:
        time.sleep(2)
        Util.Clear()
        bot = CHATBOT();