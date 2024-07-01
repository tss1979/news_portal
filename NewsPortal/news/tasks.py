from celery import shared_task
from django.core.mail import send_mail
from .models import Category, Post
import datetime


@shared_task
def send_notification_post_created(instance):
    subject = f'New - {instance.title}'
    message = 'http://127.0.0.1:8000/news/' + str(instance.pk)
    categories = instance.category.all()
    mails = []
    for category in categories:
        for user in category.user.all():
            if user.email not in mails:
                mails.append(user.email)
    send_mail(
        subject=subject,
        message=message,
        from_email='tashkinov2@gmail.com',
        recipient_list=mails
    )


@shared_task
def send_new_posts():
    message = ''
    categories = Category.objects.all()
    period = datetime.datetime.now() - datetime.timedelta(weeks=1)
    for category in categories:
        mails = [user.email for user in category.user.all()]
        posts = Post.objects.filter(created_at__gte=period)
        titles = [post.title for post in posts]
        links = ['http://127.0.0.1:8000/news/' + str(post.pk) for post in posts]
        for t, l in zip(titles, links):
            message += f'{t} - {l}\n'
        send_mail(
            subject='Greeting from NewsPortal - New Posts',
            message=message,
            from_email='tashkinov2@gmail.com',
            recipient_list=mails
        )