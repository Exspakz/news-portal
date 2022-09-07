from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.urls import reverse_lazy

from news.models import Author
from .forms import ProfileUpdateForm
from .mixins import ProfileRequiredMixin


class UserProfileUpdate(ProfileRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'account/profile_update.html'
    success_url = reverse_lazy('home')


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        if not hasattr(user, 'author'):
            Author.objects.create(
                authorUser=User.objects.get(pk=user.id)
            )
    return redirect('/')
