from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin


class NextGenPermissionRequiredMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        raise ValueError('Invalid request')

    def has_permission(self):
        """
        Overriding this method to customize the way permissions are checked.
        """
        perms = super().get_permission_required()
        return self.request.user.has_perms(perms)
