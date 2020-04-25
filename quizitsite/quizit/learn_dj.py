
import random
import pandas as pd

from quizit.models import Item, Response
from quizit.format import Format
from quizit.learn import Learn

class LearnDJ(object):

    def get_item(self, user_email):
        return self.get_simple_smart_item(user_email)

    def get_item_by_id(self, item_id):
        return Item.objects.get(pk=item_id)

    def get_random_item(self, n=20):
        item_id = random.randint(0, n)
        return self.get_item_by_id(item_id)

    def get_all_items(self):
        return Item.objects.all()

    def get_user_responses(self, user_email):
        return Response.objects.filter(user=user_email)

    def get_user_responses_df(self, user_email):
        responses = Response.objects.filter(user=user_email)
        resp_list = [r.to_dict() for r in responses]
        resp_df = pd.DataFrame(resp_list)
        return resp_df

    def get_item_df(self):
        items = Item.objects.all()
        item_list = [r.to_dict() for r in items]
        item_df = pd.DataFrame(item_list)
        return item_df

    def get_simple_smart_item(self, user_email):
        
        # get all items and user responses
        items_df = self.get_item_df()
        responses_df = self.get_user_responses_df(user_email)

        # pick item
        learn = Learn() 
        item_row = learn.simple(items_df, responses_df)
        print(item_row)
        picked_item = Item.objects.get(key=item_row['key'])
        
        return picked_item

    def create_feedback(self, correct, item, answer):
        # TODO: move this in the learn as this is not DJ specific
        
        if correct:
            feedback = 'Correct: ' + item.question + ' = ' + item.answer
        else:
            feedback = 'Nope: ' + item.question + ' = ' + item.answer
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
        r.key = i.question + '|' + i.answer
        r.correct = correct
        r.user = email
        r.save()

    # def get_first_item(self):
    #     item = Item.objects.all()[0]       
    #     return item
