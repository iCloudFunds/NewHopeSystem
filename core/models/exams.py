from django.db import models
from core.models.std import Student
from core.models.academics import Subject

class Examination(models.Model):
    name = models.CharField(max_length=100)
    term = models.IntegerField(default=1)
    academic_year = models.CharField(max_length=10, default="2024/2025")

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)