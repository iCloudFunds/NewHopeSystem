from django.db import models

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('INDUSTRIAL', 'Industrial'),
        ('GENERAL', 'General'),
        ('COMMERCIAL', 'Commercial'),
    ]
    
    name = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
    
    @property
    def teacher_count(self):
        """Return the number of teachers in this department"""
        return self.teacher_set.count()
    
    @property
    def class_count(self):
        """Return the number of classes in this department"""
        return self.schoolclass_set.count()
    
    @property
    def student_count(self):
        """Return the number of students in this department (through their classes)"""
        from .student import Student
        return Student.objects.filter(current_class__department=self).count()