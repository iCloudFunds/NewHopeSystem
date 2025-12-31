from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
import datetime
from django.core.exceptions import ValidationError

class Student(models.Model):
    # Link to admin user (for login/authentication - admin only)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # Auto-generated Student ID
    student_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    
    # Student Information
    full_name = models.CharField(max_length=200, verbose_name="FULL NAMES")
    
    # Date validation: DOB cannot be today
    date_of_birth = models.DateField(
        verbose_name="DATE OF BIRTH",
        help_text="Cannot be today's date"
    )
    
    # Admission date can be today
    date_of_admission = models.DateField(
        verbose_name="DATE OF ADMISSION",
        auto_now_add=False,  # We'll set default but allow editing
        default=datetime.date.today
    )
    
    # Parent/Guardian Information (replaces emergency_contact)
    parent_guardian_name = models.CharField(
        max_length=200, 
        verbose_name="Parent/Guardian FULL NAME",
        blank=True
    )
    parent_guardian_contact = models.CharField(
        max_length=20, 
        verbose_name="Parent/Guardian CONTACT",
        blank=True
    )
    
    # Other Information
    address = models.TextField(blank=True)
    current_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    class Meta:
        ordering = ['student_id']
    
    def clean(self):
        """Validate that date of birth is not today"""
        if self.date_of_birth and self.date_of_birth == datetime.date.today():
            raise ValidationError({
                'date_of_birth': 'Date of birth cannot be today.'
            })
    
    def save(self, *args, **kwargs):
        # Generate student ID only if it doesn't exist
        if not self.student_id:
            current_year = datetime.date.today().year
            
            # Find the highest sequence number for this year
            latest_id = Student.objects.filter(
                student_id__startswith=f'NHC-{current_year}-'
            ).aggregate(Max('student_id'))['student_id__max']
            
            if latest_id:
                # Extract the sequence number and increment it
                sequence = int(latest_id.split('-')[-1]) + 1
            else:
                sequence = 1
            
            # Format: NHC-2024-001
            self.student_id = f'NHC-{current_year}-{sequence:03d}'
        
        # Run validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"