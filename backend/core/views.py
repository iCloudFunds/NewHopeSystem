from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from backend.core.models import Student, Teacher, Class, Department, Subject
# --- Public Views ---

class HomeView(TemplateView):
    """Main homepage view"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home - New Hope System'
        context['welcome_message'] = 'Welcome to New Hope School Management System'
        return context

class AboutView(TemplateView):
    """About page view"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us - New Hope System'
        return context

class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'core/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us - New Hope System'
        context['contact_info'] = {
            'phone': '+237652924816',
            'whatsapp': '+237671322472',
            'email': 'nde.kenneth61@gmail.com'
        }
        return context

# --- Protected Views (Require Login) ---

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """User dashboard view"""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dashboard - New Hope System'
        context['user'] = self.request.user
        return context

class StudentsListView(LoginRequiredMixin, TemplateView):
    """List all students"""
    template_name = 'core/students.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all().order_by('student_id')
        
        paginator = Paginator(students, 20)
        page = self.request.GET.get('page')
        student_list = paginator.get_page(page)
        
        context.update({
            'page_title': 'Students - New Hope System',
            'students': student_list,
            'total_students': students.count(),
        })
        return context

class TeachersListView(LoginRequiredMixin, TemplateView):
    """List all teachers"""
    template_name = 'core/teachers.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teacher.objects.all().order_by('teacher_id')
        
        paginator = Paginator(teachers, 20)
        page = self.request.GET.get('page')
        teacher_list = paginator.get_page(page)
        
        context.update({
            'page_title': 'Teachers - New Hope System',
            'teachers': teacher_list,
            'total_teachers': teachers.count(),
        })
        return context

class ClassesListView(LoginRequiredMixin, TemplateView):
    """List all classes"""
    template_name = 'core/classes.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes = Class.objects.all().order_by('name')
        
        context.update({
            'page_title': 'Classes - New Hope System',
            'classes': classes,
            'total_classes': classes.count(),
        })
        return context

class DepartmentsListView(LoginRequiredMixin, TemplateView):
    """List all departments"""
    template_name = 'core/departments.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = Department.objects.all().order_by('name')
        
        context.update({
            'page_title': 'Departments - New Hope System',
            'departments': departments,
            'total_departments': departments.count(),
        })
        return context

class ReportsView(LoginRequiredMixin, TemplateView):
    """Reports dashboard"""
    template_name = 'core/reports.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'page_title': 'Reports & Analytics - New Hope System',
            'student_count': Student.objects.count(),
            'teacher_count': Teacher.objects.count(),
            'class_count': Class.objects.count(),
            'department_count': Department.objects.count(),
            'subject_count': Subject.objects.count(),
            'recent_students': Student.objects.all().order_by('-date_of_admission')[:5],
        })
        return context

# --- Utility & Error Views ---

def test_static(request):
    return render(request, 'core/test_static.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)