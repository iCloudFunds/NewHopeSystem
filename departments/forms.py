from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from backend.core.models import Department
from .models import Stream, Floor, UserProfile

# Simple form for Principal login
class PrincipalLoginForm(AuthenticationForm):
    pass

# Simple form for Teacher login
class TeacherLoginForm(AuthenticationForm):
    pass

class AdminLoginForm(AuthenticationForm):
    ROLE_CHOICES = [
        ('', 'Select Role'),
        ('Vice Principal', 'Vice Principal'),
        ('Chief of Works', 'Chief of Works'),
        ('Discipline Master', 'Discipline Master'),
        ('Senior Discipline Master', 'Senior Discipline Master'),
        ('Secretary', 'Secretary'),
        ('Accountant', 'Accountant'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="Select Department")
    stream = forms.ModelChoiceField(queryset=Stream.objects.all(), required=False, empty_label="Select Stream")
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), required=False, empty_label="Select Floor")
    stream_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Stream Password")
    department_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Department Password")
    floor_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Floor Password")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure querysets are fresh and point to all objects
        self.fields['department'].queryset = Department.objects.all()
        self.fields['stream'].queryset = Stream.objects.all()
        self.fields['floor'].queryset = Floor.objects.all()
        
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'Vice Principal':
            department = cleaned_data.get('department')
            stream = cleaned_data.get('stream')
            stream_password = cleaned_data.get('stream_password')
            
            if not department:
                self.add_error('department', 'Department is required for Vice Principal.')
            elif department.name != 'General':
                self.add_error('department', 'Vice Principal can only be in General department.')
            
            if not stream:
                self.add_error('stream', 'Stream is required for Vice Principal.')
            
            if not stream_password:
                self.add_error('stream_password', 'Stream password is required for Vice Principal.')
        
        elif role == 'Chief of Works':
            department = cleaned_data.get('department')
            department_password = cleaned_data.get('department_password')
            
            if not department:
                self.add_error('department', 'Department is required for Chief of Works.')
            elif department.name not in ['Industrial', 'Commercial']:
                self.add_error('department', 'Chief of Works can only be in Industrial or Commercial department.')
            
            if not department_password:
                self.add_error('department_password', 'Department password is required for Chief of Works.')
        
        elif role == 'Discipline Master':
            floor = cleaned_data.get('floor')
            if not floor:
                self.add_error('floor', 'Floor is required for Discipline Master.')
        
        return cleaned_data

# Department creation form
class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
        }

# Department edit form
class DepartmentEditForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
        }

# Stream creation form
class StreamCreationForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['name', 'department']

# Floor creation form
class FloorCreationForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['name', 'description', 'floor_password']

# User creation form for Principal
class UserCreationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[
        ('Vice Principal', 'Vice Principal'),
        ('Chief of Works', 'Chief of Works'),
        ('Discipline Master', 'Discipline Master'),
        ('Senior Discipline Master', 'Senior Discipline Master'),
        ('Secretary', 'Secretary'),
        ('Accountant', 'Accountant'),
        ('Teacher', 'Teacher'),
    ])
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

# User edit form
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

# Quick create form for classes
class ClassCreationForm(forms.Form):
    name = forms.CharField(max_length=100)
    level = forms.ChoiceField(choices=[('Form 1', 'Form 1'), ('Form 2', 'Form 2'), ('Form 3', 'Form 3'), ('Form 4', 'Form 4')])
    stream = forms.CharField(max_length=10)
    academic_year = forms.CharField(max_length=20)