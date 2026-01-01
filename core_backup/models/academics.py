from django.db import models

class Classroom(models.Model):
    LEVEL_CHOICES = [
        ('O', 'Ordinary Level'),
        ('A', 'Advanced Level'),
    ]
    
    DEPT_CHOICES = [
        ('COM', 'Commercial'),
        ('IND', 'Industrial'),
        ('GEN', 'General'),
    ]

    STREAM_CHOICES = [
        ('ARTS', 'General Arts'),
        ('SCI', 'General Science'),
        ('NONE', 'N/A'),
    ]

    name = models.CharField(max_length=50, unique=True, help_text="e.g., Form 1, Upper Sixth")
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    department = models.CharField(max_length=3, choices=DEPT_CHOICES)
    stream = models.CharField(max_length=4, choices=STREAM_CHOICES, default='NONE')
    capacity = models.IntegerField(default=40)

    def __str__(self):
        if self.department == 'GEN':
            return f"{self.name} ({self.get_stream_display()})"
        return f"{self.name} ({self.get_department_display()})"

class Subject(models.Model):
    # This links the subject directly to ONE specific classroom
    classroom = models.ForeignKey(
        Classroom, 
        on_delete=models.CASCADE, 
        related_name='class_subjects'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name