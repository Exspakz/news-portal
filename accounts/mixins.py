from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().id == self.request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
