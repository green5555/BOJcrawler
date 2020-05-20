import requests
from bs4 import BeautifulSoup
from django.http import Http404
import time 

from personalPage.models import Member, Problem, Acceptance, HongikSolvedProblem, HongikNotSolvedProblem

class UserPageCrawler :

    def __init__(self, BOJid, accept_number) : 
        self.BOJid = BOJid
        self.accept_number = accept_number
    
    def crawl(self):

        myMember = Member.objects.update_or_create(BOJid = self.BOJid, defaults={'BOJid':self.BOJid, 'accept_number':self.accept_number})[0]
        myAcceptSet = set([accept.problem_index for accept in Acceptance.objects.filter(member_key=myMember)])

        url = 'https://www.acmicpc.net/user/' + self.BOJid
        requested = requests.get(url)
        if requested.status_code >= 400 :
            raise Http404("BOJ에 그런 아이디는 존재하지 않아요")

        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')
        selector = 'body > div.wrapper > div.container.content > div.row > div:nth-of-type(2) > div:nth-of-type(3) > div.col-md-9 > div:nth-of-type(1) > div.panel-body > span'
        tag_list = mySoup.select(selector)

        for i in range(0, len(tag_list), 2) :
            index = int(tag_list[i].get_text())
            myAcceptSet.discard(index)
            try :
                myProblem = Problem.objects.get(index = index)
            except :
                print('fail to find problem {} while crawl user page'.format(index))
                continue

            if index not in myAcceptSet :
                Acceptance.objects.create(member_key = myMember, problem_key = myProblem, member_BOJid=self.BOJid, problem_index=index)
            
        #delete these accept
        for index in myAcceptSet :
            Acceptance.objects.filter(member_BOJid = self.BOJid, problem_index = index).delete()



class HongikPageCrawler :

    def crawl_page(self, page) :
        url = 'https://www.acmicpc.net/school/ranklist/436/' + str(page)
        requested = requests.get(url)
        if requested.status_code >= 400 :
            return False
        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')

        selector = '#ranklist > tbody > tr'
        crawled_list = mySoup.select(selector)
        for tags in crawled_list :
            BOJid = tags.select_one('td:nth-child(2)>a').get_text()
            accept_number = tags.select_one('td:nth-child(4)>a').get_text()
            try :
                mem = Member.objects.get(BOJid = id)
                if mem.accept_number != accept_number :
                    raise
            except :
                UserPageCrawler(BOJid, accept_number).crawl()
                
        return True

    def crawl_all_pages(self) :
        pageCnt = 1
        now = time.time()
        while pageCnt <= 50 :
            if self.crawl_page(pageCnt) == False :
                break
            print('HongikPageCrawler - crawl page {} / time = {}'.format(pageCnt, now - time.time()))

class ProblemPageCrawler:

    def crawl_page(self, page) :
        url = 'https://www.acmicpc.net/problemset/' + str(page)
        requested = requests.get(url)
        if requested.status_code >= 400 :
            return False
        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')

        selector = '#problemset > tbody > tr'
        crawled_list = mySoup.select(selector)
        for tags in crawled_list :
            index = tags.select_one('td:nth-child(1)').get_text()
            title = tags.select_one('td:nth-child(2)').get_text()
            solved_number = tags.select_one('td:nth-child(4)').get_text()

            Problem.objects.update_or_create(index = index, defaults={'title':title, 'solved_number':solved_number},)
        return True

    def crawl_all_pages(self):
        pageCnt = 1
        now = time.time()
        while pageCnt <= 1000 :
            if self.crawl_page(pageCnt) == False :
                break
            time.sleep(1.0)
            print('ProblemPageCrawler - crawl page {} / time = {}'.format(pageCnt, now - time.time()))

'''
class ProblemCrawler:
    def __init__(self, number):
        self.number = number
        self.title = ''
        self.solveNumber = 0

    def crawl(self):
        url = 'https://www.acmicpc.net/problem/' + str(self.number)
        requested = requests.get(url)
        if requested.status_code >= 400 :
            raise Http404("존재하지 않은 문제에 접근했어요")
        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')

        self.title = mySoup.select_one('#problem_title').text
        self.solveNumber = (mySoup.select_one('#problem-info > tbody > tr > td:nth-child(5)').text)
'''
        
'''
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
'''