from django.db import models

# Create your models here.
class Member(models.Model):
    BOJid = models.CharField(blank=False, max_length=100, null=False, unique=True)

class Acceptance(models.Model):
    who = models.ForeignKey('Member', on_delete=models.CASCADE)
    solved = models.ForeignKey('Problem', on_delete=models.CASCADE)
    solvedNumber = models.IntegerField(blank=False)

class Problem(models.Model):
    number = models.IntegerField(blank=False)
    title = models.CharField(max_length=100, null=False, default="")
   # who = models.ForeignKey('Member', on_delete=models.CASCADE)