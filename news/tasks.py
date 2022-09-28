from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task

from datetime import datetime, timedelta

from .models import *


@shared_task
def notify_subscribers_for_new_post(id, title, text):

    site = Site.objects.get_current()
    link = f'http://{site.domain}:8000/news/{id}'

    mailing_list = list(
        PostCategory.objects.filter(
            postThrough_id=id
        ).values_list(
            'categoryThrough__subscribers__username',
            'categoryThrough__subscribers__first_name',
            'categoryThrough__subscribers__email',
            'categoryThrough__name',
        )
    )

    for user, first_name, email, category in mailing_list:
        if not first_name:
            first_name = user

        html_content = render_to_string(
            'account/email/email_post_create_message.html',
            {
                'name': first_name,
                'category': category,
                'title': title,
                'text': text,
                'site_name': site.name,
                'link': link,
            }
        )

        message = EmailMultiAlternatives(
            subject=f'{site.name}! '
                    f'New post in category "{category}"',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]

        )
        message.attach_alternative(html_content, 'text/html')
        message.send()


@shared_task
def notify_subscribers_about_weekly_news():
    site = Site.objects.get_current()

    for category in Category.objects.all():

        mailing_list = list(
            SubscribeCategory.objects.filter(
                categoryThrough=category
            ).values_list(
                'userThrough__username',
                'userThrough__first_name',
                'userThrough__email',
                'categoryThrough__name'
            )
        )

        posts_list = list(
            category.post_set.filter(
                dateCreation__gt=datetime.utcnow() - timedelta(days=7)
            ).values_list('id', 'title'))

        if len(mailing_list) > 0 and len(posts_list) > 0:

            print('Mailing_list:', mailing_list)
            print('-' * 50)
            print('Posts_list:', posts_list)

            for user, first_name, email, category_name in mailing_list:
                if not first_name:
                    first_name = user

                html_content = render_to_string(
                    'account/email/email_post_last_weak_message.html',
                    {
                        'name': first_name,
                        'category': category,
                        'site': site,
                        'posts': posts_list,
                    }
                )

                message = EmailMultiAlternatives(
                    subject=f'{site.name}! '
                            f'All news in the last week in category"{category}"',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]

                )
                message.attach_alternative(html_content, 'text/html')
                message.send()
