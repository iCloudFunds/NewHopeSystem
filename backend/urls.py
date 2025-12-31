"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from departments.views import home_page, chat_room  # Added chat_room here
from .core import views

urlpatterns = [
    # Home page
    path('', home_page, name='home'),
    
    # Chat Room (New Real-time Feature)
    path('chat/', chat_room, name='chat_room'),
    
    # Include departments app URLs
    path('', include('departments.urls')),
    
    # Existing core app pages
    path('home-old/', views.HomeView.as_view(), name='home_old'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # New pages
    path('students/', views.StudentsListView.as_view(), name='students'),
    path('teachers/', views.TeachersListView.as_view(), name='teachers'),
    path('classes/', views.ClassesListView.as_view(), name='classes'),
    path('departments-list/', views.DepartmentsListView.as_view(), name='departments_list'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    # Admin
    path('admin/', admin.site.urls),
]

# Custom error handlers
handler404 = 'backend.core.views.handler404'
handler500 = 'backend.core.views.handler500'