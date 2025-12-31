from django.urls import path
from . import views

urlpatterns = [
    # Home page and login URLs
    path('', views.home_page, name='home'),
    path('admin-login/', views.custom_admin_login, name='admin_login'),
    path('principal-login/', views.principal_login, name='principal_login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    
    # Dashboard router
    path('dashboard/', views.dashboard_router, name='dashboard_router'),
    
    # ==================== NEW DASHBOARD URLS ====================
    path('principal-dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('vice-principal-dashboard/', views.vice_principal_dashboard, name='vice_principal_dashboard'),
    path('chief-of-works-dashboard/', views.chief_of_works_dashboard, name='chief_of_works_dashboard'),
    path('discipline-master-dashboard/', views.discipline_master_dashboard, name='discipline_master_dashboard'),
    path('secretary-dashboard/', views.secretary_dashboard, name='secretary_dashboard'),
    path('accountant-dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # ==================== SETUP VIEWS ====================
    path('create-initial-departments/', views.create_initial_departments, name='create_initial_departments'),
    path('create-department/', views.create_department_view, name='create_department'),
    path('edit-department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('create-user/', views.create_user_view, name='create_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('create-class/', views.create_class_view, name='create_class'),
    
    # ==================== DASHBOARD FORM HANDLERS ====================
    path('request-stream-change/', views.request_stream_change, name='request_stream_change'),
    path('request-password-change/', views.request_password_change, name='request_password_change'),
    path('send-parent-announcement/', views.send_parent_announcement, name='send_parent_announcement'),
    path('update-department-settings/', views.update_department_settings, name='update_department_settings'),
    path('schedule-workshop/', views.schedule_workshop, name='schedule_workshop'),
    path('request-department-password-change/', views.request_department_password_change, name='request_department_password_change'),
    path('report-incident/', views.report_incident, name='report_incident'),
    path('record-positive-behavior/', views.record_positive_behavior, name='record_positive_behavior'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('record-payment/', views.record_payment, name='record_payment'),
    path('create-lesson-plan/', views.create_lesson_plan, name='create_lesson_plan'),
    
    # ==================== LEGACY DASHBOARD URLS ====================
    path('general/', views.general_dashboard, name='general_dashboard'),
    path('industrial/', views.industrial_dashboard, name='industrial_dashboard'),
    path('commercial/', views.commercial_dashboard, name='commercial_dashboard'),
    path('discipline/', views.discipline_dashboard, name='discipline_dashboard'),
    path('senior-discipline/', views.senior_discipline_dashboard, name='senior_discipline_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # System URLs
    path('logout/', views.custom_logout, name='logout'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),

    # ==================== CHAT SYSTEM URLS ====================
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/private/<int:user_id>/', views.private_chat, name='private_chat'),
    path('chat/upload/', views.upload_chat_file, name='upload_chat_file'),
    path('staff-chat/', views.staff_chat_dashboard, name='staff_chat_dashboard'),
]