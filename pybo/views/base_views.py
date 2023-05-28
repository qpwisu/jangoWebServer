import logging

from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question

logger = logging.getLogger('pybo')


def index(request):
    logger.info("INFO 레벨로 출력")
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}  # <------ so 추가
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so','recent')
    comment_list = question.comment_set.all()
    #정렬
    if so == 'recent':
        comment_list = comment_list.order_by( '-create_date')
    else: #recommend
        comment_list = comment_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    paginator = Paginator(comment_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    question.viewers+=1
    context = {'question': question,'comment_list': page_obj, 'page': page, 'so': so}
    question.save()
    return render(request, 'pybo/question_detail.html', context)