from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Item(models.Model):

    topic = models.CharField(max_length=100)
    index = models.IntegerField()
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    key = models.CharField(max_length=801)
    tags = models.CharField(max_length=400)
    alts = models.CharField(max_length=800)

    def __repr__(self):
        return '; '.join([self.question,
                          self.answer, 
                          self.key])
    
    def __str__(self):
        return self.__repr__()

    def to_list(self):
        return [self.topic, self.index, self.question, 
                self.answer, self.key, self.tags]

    def to_dict(self):
        return {'topic': self.topic, 
                'index': self.index, 
                'question': self.question, 
                'answer': self.answer, 
                'key': self.key, 
                'tags': self.tags,
                'alts': self.alts}

class Response(models.Model):

    topic = models.CharField(max_length=100)
    correct = models.BooleanField()
    key = models.CharField(max_length=801)
    ts = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=600)
    # user_dj = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __repr__(self):
        return '; '.join([self.user,
                          str(self.ts), 
                          self.key,
                          str(self.correct)])

    def __str__(self):
        return self.__repr__()

    def to_list(self):
        return [self.topic, self.correct, self.key, self.ts, self.user]

    def to_dict(self):
        return {'topic': self.topic, 
                'correct': self.correct, 
                'key': self.key, 
                'ts': self.ts, 
                'user': self.user
                }