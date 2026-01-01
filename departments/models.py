from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Stream(models.Model):
    STREAM_CHOICES = [
        ('first_cycle', 'First Cycle'),
        ('second_cycle', 'Second Cycle'),
    ]
    
    name = models.CharField(max_length=50, choices=STREAM_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['name', 'department']
    
    def __str__(self):
        return f"{self.get_name_display()} ({self.department.name})"

class Floor(models.Model):
    FLOOR_CHOICES = [
        ('down', 'Down Floor'),
        ('middle', 'Middle Floor'),
        ('top', 'Top Floor'),
    ]
    
    name = models.CharField(max_length=50, choices=FLOOR_CHOICES, unique=True)
    description = models.CharField(max_length=200, blank=True)
    floor_password = models.CharField(max_length=128, blank=True)  # Hashed password
    
    def __str__(self):
        return self.get_name_display()

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('Chief of Works', 'Chief of Works'),
        ('Discipline Master', 'Discipline Master'),
        ('Senior Discipline Master', 'Senior Discipline Master'),
        ('Secretary', 'Secretary'),
        ('Accountant', 'Accountant'),
        ('Teacher', 'Teacher'),
    ]
    
    # Changed User to settings.AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    is_senior_discipline_master = models.BooleanField(default=False)
    stream_password = models.CharField(max_length=128, blank=True)  # Hashed password
    department_password = models.CharField(max_length=128, blank=True)  # Hashed password
    floor_password = models.CharField(max_length=128, blank=True)  # Hashed password
    can_switch_departments = models.BooleanField(default=False)
    finance_access = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Message(models.Model):
    # Changed User to settings.AUTH_USER_MODEL
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

class UserStatus(models.Model):
    # Changed User to settings.AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"