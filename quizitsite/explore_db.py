#!/usr/bin/env python

from quizit.models import Item, Response

def get_items():
    return Item.objects.all()

def get_responses():
    return Response.objects.all()

def status():

    items = get_items()
    responses = get_responses()

    for r in responses:
        print(r)

status()