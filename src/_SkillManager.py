import os
from src.Skills.tell_name import name
import sys, traceback

from src.Skills.greet import greet
from src.Skills.see_menu import menu
from src.Skills.add_order import add_order
from src.Skills.see_cart import cart
from src.Skills.remove_order import remove_order
from src.Skills.question_yes import question_yes
from src.Skills.question_no import question_no
from src.Skills.reset_cart import reset
from src.Skills.tell_name import name
from src.Skills.General_Questions import Gquestion
from src.Skills.checkout import checkout
 
class SKM:

    def findSkill(data):
        intent = data['input']['intent']
        try:
            switcher = {
                'greet': lambda: greet.run(data),
                'see_menu': lambda: menu.run(data),
                'add_order': lambda: add_order.run(data),
                'see_cart': lambda: cart.run(data),
                'delete_order': lambda: remove_order.run(data),
                'q_yes': lambda: question_yes.run(data),
                'q_no': lambda: question_no.run(data),
                'reset_cart': lambda: reset.run(data),
                'tell_name': lambda: name.run(data),
                'general_question': lambda: Gquestion.run(data),
                'checkout': lambda: checkout.run(data)
            }
            switch_answer = switcher[intent]()
            return switch_answer
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)
            switch_answer = data
            return switch_answer
    
    
