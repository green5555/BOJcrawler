from django.contrib import admin

# Register your models here.
from .models import Member, Problem

admin.site.register(Member)
admin.site.register(Problem)