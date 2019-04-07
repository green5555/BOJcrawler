from django.db import models

# Create your models here.
class Member(models.Model):
    BOJid = models.CharField(blank=False, max_length=100, null=False, unique=True)
    accept_number = models.IntegerField()

class Acceptance(models.Model):
    member_key = models.ForeignKey('Member', on_delete=models.CASCADE)
    problem_key = models.ForeignKey('Problem', on_delete=models.CASCADE)
    member_BOJid = models.CharField(blank=False, max_length=100, null=False)
    problem_index = models.IntegerField()

class Problem(models.Model):
    index = models.IntegerField(unique = True)
    title = models.CharField(max_length=100, null=False)
    solved_number = models.IntegerField()

class HongikSolvedProblem(models.Model):
    problem_key = models.ForeignKey('Problem', on_delete=models.CASCADE)
    solved_number = models.IntegerField()

class HongikNotSolvedProblem(models.Model):
    problem_key = models.ForeignKey('Problem', on_delete=models.CASCADE)
    solved_number = models.IntegerField()

'''
Acceptance를 1시간에 1번씩 긁는다

'''