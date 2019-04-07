from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
#from .utils import ProblemCrawler, UserPageCrawler
from .models import Member, Problem, Acceptance

def query_id(request):
    if request.method == 'POST' :
        return redirect('/user/' + request.POST.get('myID'))
    if request.method == 'GET' :
        return render(request, 'query_id_page.html')
    

# TODO : 주기적으로 크롤링 하는 하는 방법 알아보기
'''
def crawling_Acceptance(myID) :

    fetched_problem_set = UserPageCrawler(myID).crawl()

    #DB에 BOJid = myID인 객체가 있나 확인, 없으면 생성
    if Member.objects.filter(BOJid = myID).exists() == False :
        Member.objects.create(BOJid = myID)

    try :
        myMember = get_object_or_404(Member, BOJid = myID)
    except :
        raise Http404("해당 멤버가 어째선지 만들어지지 않았어요..")
    
    acceptance_problem_set = set([accept.solved.number for accept in Acceptance.objects.filter(who=myMember)])

    problem_to_add_list = []
    number_to_accept_list = []
    for number_to_add in fetched_problem_set - acceptance_problem_set :
        number_to_accept_list.append(number_to_add)
        if Problem.objects.filter(number = number_to_add).exists() == False :
            myCrawler = ProblemCrawler(number_to_add)
            myCrawler.crawl()
            problem_to_add_list.append(Problem(number = myCrawler.number, title = myCrawler.title, solveNumber = myCrawler.solveNumber))
    Problem.objects.bulk_create(problem_to_add_list)

    acceptance_to_add_list = []
    for num in number_to_accept_list :
        acceptance_to_add_list.append(Acceptance(who = myMember, solved = Problem.objects.get(number = num), problemNumber = num))
    Acceptance.objects.bulk_create(acceptance_to_add_list)

    for number_to_erase in acceptance_problem_set - fetched_problem_set : 
        Acceptance.objects.get(who = myMember, solved = Problem.objects.get(number = number_to_erase)).delete()

    return myMember
    # Problem.objects.create(number = problem[0], title = problem[1], who = myMember)
'''

def view_personal_stat(request, myID):

    #if request.method == 'POST'

    #myMeber = crawling_Acceptance(myID)

    problem_list = []
    for accept in Acceptance.objects.filter(member_BOJid=myMeber).order_by('problem_index') :
        problem_list.append(accept.problem_key)
    
    data = {
        'myID' : myID,
        'problem_list' : problem_list
    }

    return render(request, 'view_personal_stat_page.html', data)