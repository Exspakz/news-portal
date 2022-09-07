from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().postAuthor.authorUser.id == self.request.user.id:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)
