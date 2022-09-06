from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm
from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm


class ProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


def add_to_group(user):
    group = Group.objects.get(name='common')
    group.user_set.add(user)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        add_to_group(user)
        return user


class BasicSocialSignupForm(SocialSignupForm):

    def save(self, request):
        user = super(BasicSocialSignupForm, self).save(request)
        add_to_group(user)
        return user
