from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post
from django.contrib.auth.models import User


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        post = instance
        subject = f'New News - {post.title}'
        message = 'http://127.0.0.1:8000/news/' + post.pk
        categories = post.category.all()
        mails = []
        for category in categories:
            for user in category.user.all():
                if user.email not in mails:
                    mails.append(user.email)

        print(post.pk, categories, mails)

        send_mail(
            subject=subject,
            message=message,
            from_email='tashkinov2@gmail.com',
            recipient_list=mails
        )


@receiver(post_save, sender=User)
def welcome_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Welcome to the NewsPortal',
            message='Greeting from The NewsPortal',
            from_email='tashkinov2@gmail.com',
            recipient_list=[instance.email]
        )



