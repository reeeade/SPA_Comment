# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import UserForm, CommentForm
from .models import Comment
from .tasks import send_notification_email


def add_comment(request, parent_id=None):
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        comment_form = CommentForm(request.POST, request.FILES)
        if user_form.is_valid() and comment_form.is_valid():
            user = user_form.save()
            comment = comment_form.save(commit=False)
            comment.user = user
            if parent:
                comment.parent = parent
            comment.save()
            if parent:
                send_notification_email.delay(comment.id)
            return redirect('comments:list')
    else:
        user_form = UserForm()
        comment_form = CommentForm(initial={'parent': parent.id if parent else None})
    return render(request, 'add_comment.html', {'user_form': user_form, 'comment_form': comment_form})


def list_comments(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if sort_order == 'asc':
        comment_list = Comment.objects.filter(parent__isnull=True).order_by(sort_by)
    else:
        comment_list = Comment.objects.filter(parent__isnull=True).order_by(f'-{sort_by}')

    paginator = Paginator(comment_list, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_comments.html',
                  {'page_obj': page_obj, 'sort_by': sort_by, 'sort_order': sort_order})
