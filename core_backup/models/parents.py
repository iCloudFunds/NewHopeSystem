from django.db import models
from django.conf import settings
from core.models.std import Student

class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='parents')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()

class ParentLoginLog(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)