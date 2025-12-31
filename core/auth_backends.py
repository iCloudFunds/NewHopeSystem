from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class ParentPortalBackend(ModelBackend):
    """
    Handles standard Admin/Staff login logic for New Hope School System.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # We define User inside the function to avoid top-level database queries
        # that crash the build process on Render.
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class StudentBackend(ModelBackend):
    """
    Custom backend for future Student features.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Note: We removed the 'from .models import Student' import from the top.
        # This prevents the "relation does not exist" error during deployment.
        return super().authenticate(request, username, password, **kwargs)