from django.urls import path
from .views import view_personal_stat, query_id

urlpatterns = [
    path('', query_id, name='query_id'),
    path('user/<str:myID>', view_personal_stat)
]