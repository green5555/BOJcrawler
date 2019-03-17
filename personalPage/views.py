from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .utils import Crawler
from .models import Member, Problem
#from .models import Favorite, Episode

# Create your views here.

def query_id(request):
    if request.method == 'POST' :
        return redirect('/user/' + request.POST.get('myID'))
    if request.method == 'GET' :
        return render(request, 'query_id_page.html')
    

# TODO : 주기적으로 크롤링 하는 하는 방법 알아보기

def view_personal_stat(request, myID):

    #if request.method == 'POST'
    myCrawler = Crawler(myID)
    fetched_problem = myCrawler.crawl()

    if myCrawler.exist == False :
        raise Http404("BOJ에 그런 아이디는 존재하지 않아요")

    #DB에 BOJid = myID인 객체가 있나 확인, 없으면 생성
    if Member.objects.filter(BOJid = myID).count() == False :
        Member.objects.create(BOJid = myID)
    
    try :
        myMember = get_object_or_404(Member, BOJid = myID)
    except :
        raise Http404("해당 멤버가 어째선지 만들어지지 않았어요..")
    
    in_DB_problem_list = Problem.objects.filter(who=myMember)
    exist_problem_set = {}
    for problem in in_DB_problem_list :
        exist_problem_set.add(problem.number)

    for problem in fetched_problem :
        if problem[0] not in exist_problem_set:
            Problem.objects.create(number = problem[0], title = problem[1], who = myMember)

    data = {
        'myID' : myID,
        'problem_list' : Problem.objects.filter(who=myMember).order_by('number')
    }
    return render(request, 'view_personal_stat_page.html', data)