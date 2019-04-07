from background_task import background
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
import requests

from personalPage.models import Problem
from .utils import ProblemPageCrawler, HongikPageCrawler

from bs4 import BeautifulSoup
from datetime import timedelta

'''
@background(schedule=10)
def hello():
    print('hello')

@login_required
def test(reqeust):
    hello()
    return HttpResponse("Good!")
'''

#페이지 로드 후 10초 후 예약
@background(schedule=10)
def do_crawl_all_problem(reapeat = 60*60*24):
    pass
    
@login_required
def crawl_all_problem(request):
    do_crawl_all_problem()
    return HttpResponse("OK!")

def test_crawl(request):
    #p = ProblemPageCrawler()
    #p.crawl_page(1)
    HongikPageCrawler().crawl_page(1)

    return HttpResponse("OK!")
    