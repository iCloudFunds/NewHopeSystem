from django.db import models
from django.conf import settings
from django.db.models import Max
import datetime
from django.core.exceptions import ValidationError

class Student(models.Model):
    """
    Student model for the core application.
    Linked to the custom User model defined in AUTH_USER_MODEL.
    """
    # Link to custom user model (core.User)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    
    # Auto-generated Student ID: e.g., NHC-2024-001
    student_id = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False, 
        blank=True
    )
    
    # Student Information
    full_name = models.CharField(max_length=200, verbose_name="FULL NAMES")
    
    date_of_birth = models.DateField(
        verbose_name="DATE OF BIRTH",
        help_text="Cannot be today's date"
    )
    
    date_of_admission = models.DateField(
        verbose_name="DATE OF ADMISSION",
        default=datetime.date.today
    )
    
    # Parent/Guardian Information
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
    
    # Address
    address = models.TextField(blank=True)
    
    # Relationship to Class using string reference to avoid Circular Import/Conflicts
    current_class = models.ForeignKey(
        'core.Class', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )
    
    class Meta:
        # CRITICAL: This tells Django exactly which app this belongs to
        app_label = 'core'
        ordering = ['student_id']
    
    def clean(self):
        """Validate that date of birth is not today"""
        if self.date_of_birth and self.date_of_birth == datetime.date.today():
            raise ValidationError({
                'date_of_birth': 'Date of birth cannot be today.'
            })
    
    def save(self, *args, **kwargs):
        """Generate student ID and save"""
        if not self.student_id:
            current_year = datetime.date.today().year
            
            # Find the highest sequence number for this year
            # We use self.__class__ to avoid importing Student directly inside its own method
            latest_id = self.__class__.objects.filter(
                student_id__startswith=f'NHC-{current_year}-'
            ).aggregate(Max('student_id'))['student_id__max']
            
            if latest_id:
                try:
                    # Extract the sequence number from 'NHC-2024-001' and increment
                    sequence = int(latest_id.split('-')[-1]) + 1
                except (ValueError, IndexError):
                    sequence = 1
            else:
                sequence = 1
            
            self.student_id = f'NHC-{current_year}-{sequence:03d}'
        
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"