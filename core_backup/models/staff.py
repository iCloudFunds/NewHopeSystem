from django.db import models
from django.conf import settings

class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    job_title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"