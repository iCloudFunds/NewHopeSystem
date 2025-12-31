from django.db import models
from .department import Department

class Subject(models.Model):
    # Link to which department offers this subject
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    
    # Subject name (e.g., Mathematics, English Language, Physics)
    name = models.CharField(max_length=100)
    
    # Subject code (e.g., MATH101, ENG201) - can be auto-generated or manual
    code = models.CharField(max_length=20, unique=True)
    
    # Which class levels this subject is taught at
    # Ordinary Level (Forms 1-5) or Advanced Level (Sixth Form)
    LEVEL_CHOICES = [
        ('ORDINARY', 'Ordinary Level (Forms 1-5)'),
        ('ADVANCED', 'Advanced Level (Sixth Form)'),
        ('BOTH', 'Both Levels'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='ORDINARY')
    
    # Whether this is a core (compulsory) or elective subject
    TYPE_CHOICES = [
        ('CORE', 'Core Subject'),
        ('ELECTIVE', 'Elective Subject'),
    ]
    subject_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='CORE')
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.department.name})"
    
    class Meta:
        ordering = ['department', 'code']