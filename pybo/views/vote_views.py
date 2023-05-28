from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer, Comment


@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, "본인이 작성한 글은 추천할 수 없습니다")
    else:
        voter_list = question.voter.filter(username=request.user).first()
        if request.user == voter_list: #두번 추천시 제거
            question.voter.remove(request.user)
        else:
            question.voter.add(request.user)
    return redirect("pybo:detail",question_id=question_id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, "본인이 작성한 글은 추천할 수 없습니다")
    else:
        voter_list = answer.voter.filter(username=request.user).first()
        if request.user == voter_list: #두번 추천시 제거
            answer.voter.remove(request.user)
        else:
            answer.voter.add(request.user)
    return redirect("pybo:detail",question_id=answer.question.id)

@login_required(login_url='common:login')
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, "본인이 작성한 글은 추천할 수 없습니다")
    else:
        voter_list = comment.voter.filter(username=request.user).first()
        if request.user == voter_list: #두번 추천시 제거
            comment.voter.remove(request.user)
        else:
            comment.voter.add(request.user)
    return redirect("pybo:detail",question_id=comment.question.id)