from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class DisciplineRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='discipline_records')
    incident_date = models.DateField()
    description = models.TextField()
    action_taken = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.student.student_id} - {self.incident_date}"