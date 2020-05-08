
from django.shortcuts import render
from django.http import HttpResponse

# post related imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from quizit.learn_dj import LearnDJ

from quizit.models import Message

def index(request):
    return HttpResponse("QuizIt app index")

def about(request):
    return render(request, 'quizit/about.html')

@login_required
def basic(request, item_id=None):

    if request.method == 'POST':
        
        if request.POST['post_type'] == 'item_submit':

            # standard
            given_answer = request.POST['given_answer']
            prev_item_key = request.POST['item_key']
            _, feedback = LearnDJ().check(prev_item_key, given_answer, request.user.email)
    
            item = LearnDJ().get_item(request.user.email)

            arg_dict =  {'item': item, 'feedback': feedback, 'prev_item_key': prev_item_key}
            return render(request, 'quizit/basic.html', arg_dict)
        
        else:

            # flag
            # TODO: move this to Learn dj
            m = Message(user=request.user.email,
                        key=request.POST['prev_item_key'],
                        type='flag',
                        text=request.POST['feedback'])
            m.save()

            # TODO: fix side effect this also gets a new item

    item = LearnDJ().get_item(request.user.email)

    arg_dict = {'item': item, 'feedback': '', 'prev_item_key': ''}
    return render(request, 'quizit/basic.html', arg_dict)
