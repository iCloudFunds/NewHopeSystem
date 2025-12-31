from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
import datetime
from .department import Department
from .subject import Subject

class Teacher(models.Model):
    # Link to Django User for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    
    # Auto-generated Teacher ID
    teacher_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200, verbose_name="FULL NAMES")
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)
    
    # Employment Information
    employment_date = models.DateField(auto_now_add=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Subjects the teacher specializes in (can teach multiple subjects)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    
    # Teacher Status
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('RESIGNED', 'Resigned'),
        ('RETIRED', 'Retired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Qualifications
    qualifications = models.TextField(blank=True, help_text="List degrees, certificates, etc.")
    
    # Additional Information
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['teacher_id']
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
    
    def save(self, *args, **kwargs):
        # Generate teacher ID only if it doesn't exist
        if not self.teacher_id:
            current_year = datetime.date.today().year
            
            # Find the highest sequence number for this year
            latest_id = Teacher.objects.filter(
                teacher_id__startswith=f'NHC-T-{current_year}-'
            ).aggregate(Max('teacher_id'))['teacher_id__max']
            
            if latest_id:
                # Extract the sequence number and increment it
                sequence = int(latest_id.split('-')[-1]) + 1
            else:
                sequence = 1
            
            # Format: NHC-T-2025-001 (T for Teacher)
            self.teacher_id = f'NHC-T-{current_year}-{sequence:03d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.teacher_id} - {self.full_name}"
    
    def get_assigned_classes(self):
        """Return all classes this teacher is assigned to"""
        return self.assigned_classes.all()