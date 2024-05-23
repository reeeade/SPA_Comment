from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment


@shared_task
def send_notification_email(comment_id):
    print(f'Starting task for comment_id: {comment_id}')
    try:
        comment = Comment.objects.get(id=comment_id)
        print(f'Comment found: {comment}')
        if comment.parent:
            parent_comment = comment.parent
            recipient_email = parent_comment.user.email
            print(f'Sending email to: {recipient_email}')
            send_mail(
                'Ответ на ваш комментарий',
                f'Пользователь {comment.user.username} ответил на ваш комментарий: {comment.text}',
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            print('Email sent successfully')
    except Comment.DoesNotExist:
        print(f'Comment with id {comment_id} does not exist')
