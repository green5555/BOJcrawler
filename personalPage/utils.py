import requests
from bs4 import BeautifulSoup
from django.http import Http404

from .models import Member, Problem

class ProblemCrawler:
    def __init__(self, number):
        self.number = number
        self.title = ''

    def crawl(self):
        url = 'https://www.acmicpc.net/problem/' + str(self.number)
        requested = requests.get(url)
        if requested.status_code >= 400 :
            raise Http404("존재하지 않은 문제에 접근했어요")
        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')

        self.title = mySoup.select_one('#problem_title').text

        

class UserPageCrawler:
    def __init__(self, myID):
        self.myID = myID

    def crawl(self):
        url = 'https://www.acmicpc.net/user/' + self.myID
        requested = requests.get(url)
        if requested.status_code >= 400 :
            raise Http404("BOJ에 그런 아이디는 존재하지 않아요")

        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')

        school_selector = '#statics > tbody > tr'
        is_hongik_flag = False
        for item in mySoup.select(school_selector) :
            if item.select_one('th').get_text() == '학교/회사' :
                if item.select_one('td > a[href = "/school/ranklist/436"]') is not None :
                    is_hongik_flag = True
        if is_hongik_flag == False :
            raise Http404('홍익대 학생만 이용할 수 있어요.')

        problem_selector = 'body > div.wrapper > div.container.content > div.row > div:nth-of-type(2) > div:nth-of-type(3) > div.col-md-9 > div:nth-of-type(1) > div.panel-body > span'
        tag_list = mySoup.select(problem_selector)
        fetched_set = set()
        for i in range(0, len(tag_list), 2) :
            number = tag_list[i].get_text()
            fetched_set.add(int(number))

        return fetched_set
    
