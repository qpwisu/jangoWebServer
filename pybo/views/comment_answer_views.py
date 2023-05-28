from django.core.checks import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from pybo.forms import CommentForm
from pybo.models import Comment,Question , Answer


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답변 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            # return redirect('pybo:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(resolve_url("pybo:detail", question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답변 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        # return redirect('pybo:detail', question_id=comment.answer.question.id)
        return redirect(
            '{}#comment_{}'.format(resolve_url("pybo:detail", question_id=comment.answer.question.id), comment.id))

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.modify_count +=1

            comment.save()
            # return redirect('pybo:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(resolve_url("pybo:detail", question_id=comment.answer.question.id), comment.id))

    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답변 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        # return redirect('pybo:detail', question_id=comment.answer.question.id)
        return redirect('{}#comment_{}'.format(resolve_url("pybo:detail", question_id=comment.answer.question.id), comment.id))

    else:
        comment.delete()
    # return redirect('pybo:detail', question_id=comment.answer.question.id)
    return redirect('{}#comment_{}'.format(resolve_url("pybo:detail", question_id=comment.answer.question.id), comment.id))
