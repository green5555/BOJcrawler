from django.urls import path
from .views import crawl_all_hongik_user, crawl_all_problem


urlpatterns = [
    path('crawl_all_hongik_user',crawl_all_hongik_user),
    path('crawl_all_problem', crawl_all_problem)
]