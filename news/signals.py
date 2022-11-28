from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Post, PostCategory
from .tasks import notify_subscribers_for_new_post


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.__class__.__name__ == 'Post':
        notify_subscribers_for_new_post.apply_async(
            (instance.id, instance.title, instance.text),
            countdown=10,
        )
