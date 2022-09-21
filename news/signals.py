from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add' and instance.__class__.__name__ == 'Post':
        notify_subscribers_for_new_post(
            instance.id, instance.title, instance.text
        )


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