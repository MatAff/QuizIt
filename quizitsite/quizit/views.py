from django.shortcuts import render
from django.http import HttpResponse

# post related imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# from quizit.models import Item
from quizit.learn_dj import LearnDJ


def index(request):
    return HttpResponse("QuizIt app index")

def about(request):
    return render(request, 'quizit/about.html')

@login_required
def basic(request, item_id=None):

    if request.method == 'POST':
        given_answer = request.POST['given_answer']
        _, feedback = LearnDJ().check(item_id, given_answer, request.user.email)
        item = LearnDJ().get_item(request.user.email)
        return render(request, 'quizit/basic.html', {'item': item, 'feedback': feedback})

    item = LearnDJ().get_item(request.user.email)
    return render(request, 'quizit/basic.html', {'item': item, 'feedback': ""})
