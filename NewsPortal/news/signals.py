from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PostCategory
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


@receiver(m2m_changed, sender=PostCategory)
def notify_managers_appointment(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
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


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    user = instance
    common_group = Group.objects.get(name='common')
    common_group.user_set.add(user)
    send_mail(
        subject='Welcome to the NewsPortal',
        message='Greeting from The NewsPortal',
        from_email='tashkinov2@gmail.com',
        recipient_list=[user.email]
    )


