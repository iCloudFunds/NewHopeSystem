# backend/core/models/__init__.py

from .student import Student
from .school_class import Class  # Import Class from its own file, NOT from student.py
from .department import Department
from .subject import Subject
from .teacher import Teacher
from .user import User
__all__ = ['Student', 'Class', 'Department', 'Subject', 'Teacher']