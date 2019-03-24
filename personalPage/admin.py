from django.contrib import admin
# Register your models here.
from .models import Member, Problem, Acceptance

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('BOJid',)

@admin.register(Acceptance)
class AcceptanceAdmin(admin.ModelAdmin):
    list_display = ('first_accept',)

    def first_accept(self, obj):
        return '{} - {}'.format(obj.who.BOJid, obj.solvedNumber)