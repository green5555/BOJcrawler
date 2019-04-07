from background_task import background
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
import requests

from personalPage.models import Problem
from .utils import ProblemPageCrawler, HongikPageCrawler

from bs4 import BeautifulSoup
from datetime import timedelta

@background(schedule=10)
def hello():
    print('hello')

@login_required
def test(reqeust):
    hello()
    return HttpResponse("Good!")

#페이지 로드 후 10초 후 예약
@background(schedule=10)
def do_crawl_all_problem(reapeat = 60*60):
    ProblemPageCrawler().crawl_all_pages()
    
@login_required
def crawl_all_problem(request):
    do_crawl_all_problem()
    return HttpResponse("OK!")

@background(schedule=10)
def do_crawl_all_hongik_user(reapeat = 60*15):
    print('go')
    HongikPageCrawler().crawl_all_pages()
    
@login_required
def crawl_all_hongik_user(request):
    do_crawl_all_hongik_user()
    return HttpResponse("OK!")
