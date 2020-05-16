
import random
import pandas as pd
import threading

from quizit.models import Item, Response, Preselect, Message
from quizit.format import Format
from quizit.learn import Learn

# import time

# def test_delayed_action():
#     print('waiting')
#     time.sleep(20)
#     print('delayed')

class LearnDJ(object):
    """Interface between django and learn.py

    Functions in this class should connect django view, the db
    and Learn functionality. All non django related functionality 
    should live in Learn.
    """

    def get_item(self, user_email):
        return self.get_simple_smart_item_async(user_email)

    def get_item_by_id(self, item_id):
        return Item.objects.get(pk=item_id)

    def get_item_by_key(self, item_key):
        return Item.objects.get(key=item_key)

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

    def get_flagged(self):
        return Message.objects.filter(type='flag')

    def get_item_df(self):
        items = Item.objects.all()
        item_list = [r.to_dict() for r in items]
        item_df = pd.DataFrame(item_list)
        return item_df

    def get_recent_responses(self, user_email, n=5):
        return Response.objects.filter(user=user_email).order_by('-id')[:n]

    def do_preselect(self, user_email, exclude=None):
        item_keys = self.get_smart_item_keys(user_email, 5, exclude)
        # print(f'item_key for preselect{"; ".join(item_keys)}')
        
        # remove current with fresh ones
        Preselect.objects.filter(user=user_email).delete()
        for key in item_keys:
            preselect = Preselect(key=key, user=user_email)
            preselect.save()

    def get_simple_smart_item_async(self, user_email):

        # get flagged responses
        flagged = self.get_flagged()
        flagged_keys = [f.key for f in flagged]
        print(f'flagged: {"; ".join(flagged_keys)}')

        # recent responses
        recent = self.get_recent_responses(user_email)
        recent_keys = [r.key for r in recent]
        print(f'recent: {"; ".join(recent_keys)}')

        # get preselected items
        preselect = Preselect.objects.filter(user=user_email)
        preselect_keys = [p.key for p in preselect]
        print(f'preselected: {"; ".join(preselect_keys)}')

        # exclude recent items
        preselect_keys = [k for k in preselect_keys if k not in recent_keys]
        print(f'preselected recent removed: {"; ".join(preselect_keys)}')

        # kick off preselection
        if len(preselect_keys) < 5:
            t = threading.Thread(target=self.do_preselect, args=[user_email, flagged_keys]) 
            t.start()

        if len(preselect_keys) > 0:
            picked_key = preselect_keys[0]
        else:
            print('WARNING: preselection was empty.')
            picked_key = self.get_smart_item_keys(self, user_email, 1, flagged_keys)[0]

        return Item.objects.get(key=picked_key)

    def get_smart_item_keys(self, user_email, n, exclude=None):
        
        item_df = self.get_item_df()
        response_df = self.get_user_responses_df(user_email)

        picked_items = Learn().simple_n(item_df, response_df, n, exclude)
        return picked_items.key.to_list()


    # def get_simple_smart_item(self, user_email, exclude=None):
        
    #     # get all items and user responses
    #     items_df = self.get_item_df()
    #     responses_df = self.get_user_responses_df(user_email)

    #     # pick item
    #     learn = Learn() 
    #     item_row = learn.simple(items_df, responses_df, exclude)
    #     picked_item = Item.objects.get(key=item_row['key'])

    #     return picked_item

    def create_feedback(self, correct, item, answer):
        # TODO: move this in the learn as this is not DJ specific
        
        if correct:
            feedback = 'Correct: ' + item.question + ' = ' + item.answer
        else:
            feedback = 'Nope: ' + item.question + ' = ' + item.answer
            feedback += '\nYou said: ' + answer
        
        return feedback

    def at_to_alt(self, answer, alts):
        if '@' in answer:
            add = [answer.replace('@', l) for l in ['o', 'a']]
            if len(alts) > 0:
                alts = '|'.join([alts, *add])
            else:
                alts = '|'.join(add)
        return alts

    def check(self, item_key, given_answer, email):
        # TODO: move none django specific functionality to learn.py
        item = self.get_item_by_key(item_key)
        answer = item.answer
        alts = item.alts
        
        # remove punctuation
        given_answer = Format.add_accents(given_answer)
        #answer = Format.remove(answer)
        #alts = Format.remove(alts)

        # remove accidentally introduced nan
        alts = alts.replace('^nan', '')

        # add @ variants
        alts = self.at_to_alt(answer, alts)

        # check answer
        correct = given_answer == answer
        if not correct and (len(alts) > 0):
            for alt in alts.split('|'):
                if given_answer == alt:
                    print('used alternative')
                    correct = True
                    break # out of for loop if one of alternative is correct
        self.save_response(item_key, correct, email)
        
        feedback = self.create_feedback(correct, item, given_answer)

        return correct, feedback

    def save_response(self, item_key, correct, email):
        
        # get item 
        i = self.get_item_by_key(item_key)

        # create response
        r = Response()
        r.key = i.question + '|' + i.answer
        r.correct = correct
        r.user = email
        r.save()

    # def get_first_item(self):
    #     item = Item.objects.all()[0]       
    #     return item
