
import random

from quizit.models import Item, Response
from quizit.format import Format
from quizit.selector import Selector

class Learn(object):

    # def get_first_item(self):
    #     item = Item.objects.all()[0]       
    #     return item

    def get_item(self, email):
        # return self.get_random_item()
        return self.get_simple_smart_item(email)

    def get_item_by_id(self, item_id):
        return Item.objects.get(pk=item_id)

    def get_random_item(self, n=20):
        item_id = random.randint(0, n)
        return self.get_item_by_id(item_id)

    def get_simple_smart_item(self, email):
        
        # pull all items
        items = Item.objects.all()

        # pull all responses
        responses = Response.objects.filter(user=email)

        # pick item
        item_key = Selector.simple(items, responses)
        picked_item = Item.objects.get(key=item_key)
        
        return picked_item

    def create_feedback(self, correct, item, answer):
        
        if correct:
            feedback = 'Correct: ' + item.question_text + ' = ' + item.answer
        else:
            feedback = 'Nope: ' + item.question_text + ' = ' + item.answer
            feedback += '\nYou said: ' + answer
        
        return feedback

    def check(self, item_id, given_answer, email):
        item = self.get_item_by_id(item_id)
        answer = item.answer
        
        # remove punctuation
        given_answer = Format.remove(given_answer)
        answer = Format.remove(answer)

        correct = given_answer == answer
        self.save_response(item_id, correct, email)
        
        feedback = self.create_feedback(correct, item, given_answer)

        return correct, feedback

    def save_response(self, item_id, correct, email):
        print('saving!')
        
        # get item 
        i = self.get_item_by_id(item_id)

        # create response
        r = Response()
        r.key = i.question_text + '|' + i.answer
        r.correct = correct
        r.user = email
        r.save()

