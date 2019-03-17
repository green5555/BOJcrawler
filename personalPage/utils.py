import requests
from bs4 import BeautifulSoup

from .models import Member, Problem

class Crawler:
    def __init__(self, myID):
        self.myID = myID
        self.exist = False

    def crawl(self):
        url = 'https://www.acmicpc.net/user/' + self.myID
        requested = requests.get(url)
        if requested.status_code >= 400 :
            return []
        self.exist = True

        html = requested.text
        mySoup = BeautifulSoup(html, 'html.parser')
        selector = 'body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div:nth-child(3) > div.col-md-9 > div:nth-child(1) > div.panel-body > span'

        tag_list = mySoup.select(selector)
        fetched_list = []
        for i in range(0, len(tag_list), 2) :
            number = tag_list[i].get_text()
            title = tag_list[i+1].get_text()
            fetched_list.append((number, title))

        return fetched_list
    
