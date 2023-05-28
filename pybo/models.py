from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    viewers = models.IntegerField(null=False, default=0)
    modify_count = models.IntegerField(null=False, default=0)
    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_count = models.IntegerField(null=False, default=0)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    voter = models.ManyToManyField(User)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    modify_count = models.IntegerField(null=False, default=0)
    question = models.ForeignKey(Question,null=True,blank=True,on_delete=models.CASCADE) # 필요한이유 코맨틀르 추가하고 question_id로 redirect 하기 위해서
    answer = models.ForeignKey(Answer,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.content