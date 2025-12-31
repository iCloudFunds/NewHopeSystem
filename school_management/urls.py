from django.contrib import admin
from django.urls import path
from core import views  

urlpatterns = [
    # 1. System Admin Panel
    path('admin/', admin.site.urls),

    # 2. Parent Portal Login Page
    path('portal/login/', views.parent_login, name='parent_login'),
    
    # 3. Parent Portal Dashboard (Now Active)
    path('portal/dashboard/', views.parent_dashboard, name='parent_dashboard'),
]