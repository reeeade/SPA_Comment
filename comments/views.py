from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, CommentForm
from .models import Comment


def add_comment(request, parent_id=None):
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        comment_form = CommentForm(request.POST)
        if user_form.is_valid() and comment_form.is_valid():
            user = user_form.save()
            comment = comment_form.save(commit=False)
            comment.user = user
            if parent:
                comment.parent = parent
            comment.save()
            return redirect('comments:list')
    else:
        user_form = UserForm()
        comment_form = CommentForm(initial={'parent': parent.id if parent else None})
    return render(request, 'add_comment.html', {'user_form': user_form, 'comment_form': comment_form})


def list_comments(request):
    comments = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
    return render(request, 'list_comments.html', {'comments': comments})