from django.db import models
from django.core.exceptions import ValidationError
from .department import Department

class Class(models.Model):
    DEPARTMENT_CATEGORIES = [
        ('GENERAL', 'General'),
        ('INDUSTRIAL', 'Industrial'),
        ('COMMERCIAL', 'Commercial'),
    ]
    
    # Streams only for Advanced Level
    SUBJECT_STREAMS = [
        ('ARTS', 'Arts'),
        ('SCIENCE', 'Science'),
        ('NONE', 'None'),
    ]
    
    # Level choices as requested
    LEVEL_CHOICES = [
        ('ADVANCED LEVEL', 'Advanced Level'),
        ('ORDINARY LEVEL', 'Ordinary Level'),
    ]
    
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='ORDINARY LEVEL')
    stream = models.CharField(max_length=10, choices=SUBJECT_STREAMS, default='NONE')
    academic_year = models.CharField(max_length=9)
    
    # Link to teachers who teach this class
    teachers = models.ManyToManyField('Teacher', related_name='assigned_classes', blank=True)
    
    class Meta:
        verbose_name_plural = "Classes"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'department', 'level', 'stream', 'academic_year'],
                name='unique_class_combo'
            )
        ]
    
    def clean(self):
        """Validate the relationship between level and stream"""
        
        # If level is ORDINARY LEVEL, stream must be NONE
        if self.level == 'ORDINARY LEVEL' and self.stream != 'NONE':
            raise ValidationError({
                'stream': 'Ordinary Level classes must have stream set to "None".'
            })
        
        # If level is ADVANCED LEVEL, stream CANNOT be NONE
        if self.level == 'ADVANCED LEVEL' and self.stream == 'NONE':
            raise ValidationError({
                'stream': 'Advanced Level classes must have a stream (Arts or Science), not "None".'
            })
    
    def save(self, *args, **kwargs):
        # Run validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.level == 'ADVANCED LEVEL' and self.stream != 'NONE':
            return f"{self.name} - {self.department.name} ({self.stream})"
        else:
            return f"{self.name} - {self.department.name}"
    
    @property
    def student_count(self):
        """Return the number of students in this class"""
        return self.students.count()
    
    @property
    def class_teacher(self):
        """Return the first teacher assigned to this class, if any"""
        return self.teachers.first()