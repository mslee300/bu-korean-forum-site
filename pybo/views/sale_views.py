from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from pybo.models import Question

from django.contrib.auth.decorators import login_required


typefield = 'sale'

@login_required(login_url='common:login')
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
  
    question_list = question_list.filter(
      Q(type__icontains=typefield) # 게시글 타입이 'info'인지 확인
    ).distinct()

    # Turn into List
    question_list = list(question_list)

    # Get most popular post
    question_obj = question_list
    max_obj = question_obj[0]
    for obj in question_obj:
      if obj.voter.count() > max_obj.voter.count():
        max_obj = obj

    # Get most commented post
    question_obj2 = question_list
    max_obj2 = question_obj2[0]
    for obj in question_obj2:
      if obj.answer_set.count() > max_obj2.answer_set.count():
        max_obj2 = obj

    # Send two items to front
    question_list.remove(max_obj2)
    if max_obj in question_list:
      question_list.remove(max_obj)
      question_list.insert(0, max_obj2)
      question_list.insert(0, max_obj)
    else:
      question_list.insert(0, max_obj2)
  
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목
            Q(content__icontains=kw) |  # 내용
            Q(answer__content__icontains=kw) |  # 답변 내용
            Q(author__username__icontains=kw) |  # 질문 글쓴이
            Q(answer__author__username__icontains=kw) # 답변 글쓴이
        ).distinct()
    paginator = Paginator(question_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list_sale.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
