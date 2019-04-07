from django.urls import path
from .views import test_crawl

urlpatterns = [
    #path('test', test, name='test'),
    #path('crawl_all_problem', crawl_all_problem)
    path('test_crawl', test_crawl)
]