from django.db import models
import pytz
import datetime

tz = pytz.timezone('Asia/Colombo')

DIFICULTIES = (
    ## value, visible choice
    ('Easy','Easy'), 
    ('Medium','Medium'), 
    ('Hard','Hard'),
)

CORRECT_ANSWER = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
)

from accounts.models import Staff, Student

class Quiz(models.Model):
    #id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFICULTIES, default='Easy')
    content = models.TextField(default="")
    answer1 = models.CharField(max_length=130, default="")
    answer2 = models.CharField(max_length=130, default="")
    answer3 = models.CharField(max_length=130, default="")
    answer4 = models.CharField(max_length=130, default="")
    correct_answer = models.IntegerField(choices=CORRECT_ANSWER, default=1)

    def __str__(self):
        return str(self.id)+'. '+self.title

## many to many relation field also do the same 
class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return f'q{self.quiz.id}-{self.student.index}'

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()

from django import forms
class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea)

## to store quiz variables
class Variable(models.Model):
    quiz_end = models.BooleanField(default=False)
    quiz_start = models.DateTimeField(default=datetime.datetime.now(tz=tz))
    ## for inheritance if variable is abstract singleton
    ##class Meta:
    ##    abstract = True
    
    def save(self, *args, **kwargs):
        self.id = 1
        super(Variable, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj