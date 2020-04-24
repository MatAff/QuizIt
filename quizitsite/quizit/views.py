from django.shortcuts import render
from django.http import HttpResponse

# post related imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# from quizit.models import Item
from quizit.learn import Learn

posts = [
    {
        'a': 'a'
    },
    {
        'a': 'b'
    }
]

def index(request):
    return HttpResponse("QuizIt app index")

def go(request):
    return render(request, 'quizit/go.html')

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'quizit/home.html', context)
    #return HttpResponse('<h1>Home</h1>')

def about(request):
    return render(request, 'quizit/about.html')

@login_required
def basic(request, feedback=None):
    print('user: ' + str(request.user.email))
    item = Learn().get_item(request.user.email)
    if feedback is None:
        feedback = ""
    return render(request, 'quizit/basic.html', {'item': item, 'feedback': feedback})


@login_required
def answer(request, item_id):
    print(item_id)
    given_answer = request.POST['given_answer']
    print(given_answer)
    correct, feedback = Learn().check(item_id, given_answer, request.user.email)
    return basic(request, feedback)
