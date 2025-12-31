from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
import random
import string
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .forms import AdminLoginForm, PrincipalLoginForm, TeacherLoginForm, DepartmentCreationForm, UserCreationForm, ClassCreationForm, UserEditForm, DepartmentEditForm
from .models import UserProfile, Department, Stream, Floor, Message, UserStatus
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

def custom_admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            department = form.cleaned_data.get('department')
            stream = form.cleaned_data.get('stream')
            floor = form.cleaned_data.get('floor')
            stream_password = form.cleaned_data.get('stream_password')
            department_password = form.cleaned_data.get('department_password')
            floor_password = form.cleaned_data.get('floor_password')
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    # Get user profile
                    profile = UserProfile.objects.get(user=user)
                    
                    # Check if user has the correct role
                    if profile.role != role:
                        form.add_error('role', f'Your account is assigned as {profile.role}, not {role}.')
                        return render(request, 'departments/custom_login.html', {'form': form})
                    
                    # Role-specific validations
                    if role == 'Vice Principal':
                        # Check if department is General
                        if not department or department.name != 'General':
                            form.add_error('department', 'Vice Principal can only be in General department.')
                        
                        # Check stream password
                        if stream_password and profile.stream_password:
                            if not check_password(stream_password, profile.stream_password):
                                form.add_error('stream_password', 'Invalid stream password.')
                        else:
                            form.add_error('stream_password', 'Stream password is required.')
                            
                        # Save stream selection
                        if stream:
                            profile.stream = stream
                            profile.save()
                    
                    elif role == 'Chief of Works':
                        # Check if department is Industrial or Commercial
                        if not department or department.name not in ['Industrial', 'Commercial']:
                            form.add_error('department', 'Chief of Works can only be in Industrial or Commercial department.')
                        
                        # Check department password
                        if department_password and profile.department_password:
                            if not check_password(department_password, profile.department_password):
                                form.add_error('department_password', 'Invalid department password.')
                        else:
                            form.add_error('department_password', 'Department password is required.')
                    
                    elif role == 'Discipline Master':
                        # Check floor password (optional)
                        if floor_password and profile.floor_password:
                            if not check_password(floor_password, profile.floor_password):
                                form.add_error('floor_password', 'Invalid floor password.')
                        
                        # Save floor selection
                        if floor:
                            profile.floor = floor
                            profile.save()
                    
                    # For Secretary and Accountant, no department selection at login
                    # For Senior Discipline Master, no floor selection at login
                    
                    # Login user
                    login(request, user)
                    
                    # Store session data for dashboard routing
                    request.session['user_role'] = role
                    request.session['user_profile_id'] = profile.id
                    
                    if department:
                        request.session['user_department'] = department.name
                    if stream:
                        request.session['user_stream'] = stream.name
                    if floor:
                        request.session['user_floor'] = floor.name
                    
                    # Redirect based on role - NOW USING NEW DASHBOARDS
                    if role == 'Principal':
                        return redirect('principal_dashboard')
                    elif role == 'Vice Principal':
                        return redirect('vice_principal_dashboard')
                    elif role == 'Chief of Works':
                        return redirect('chief_of_works_dashboard')
                    elif role == 'Discipline Master':
                        return redirect('discipline_master_dashboard')
                    elif role == 'Senior Discipline Master':
                        return redirect('discipline_master_dashboard')  # Same template, different context
                    elif role == 'Secretary':
                        return redirect('secretary_dashboard')
                    elif role == 'Accountant':
                        return redirect('accountant_dashboard')
                    
                except UserProfile.DoesNotExist:
                    form.add_error(None, 'User profile not found. Please contact administrator.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AdminLoginForm()
        # Check if role is passed in URL parameters
        role_from_url = request.GET.get('role')
        if role_from_url:
            # Set initial value for role field
            form.fields['role'].initial = role_from_url
    
    return render(request, 'departments/custom_login.html', {'form': form})

def principal_login(request):
    if request.method == 'POST':
        form = PrincipalLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    # Get user profile
                    profile = UserProfile.objects.get(user=user)
                    
                    # Check if user is a Principal
                    if profile.role != 'Principal':
                        form.add_error(None, 'This account is not authorized as Principal.')
                        return render(request, 'departments/principal_login.html', {'form': form})
                    
                    # Login user
                    login(request, user)
                    
                    # Store session data
                    request.session['user_role'] = 'Principal'
                    request.session['user_profile_id'] = profile.id
                    
                    # Redirect to principal dashboard
                    return redirect('principal_dashboard')
                    
                except UserProfile.DoesNotExist:
                    form.add_error(None, 'User profile not found. Please contact administrator.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = PrincipalLoginForm()
    
    return render(request, 'departments/principal_login.html', {'form': form})

def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    # Get user profile
                    profile = UserProfile.objects.get(user=user)
                    
                    # Check if user is a Teacher
                    if profile.role != 'Teacher':
                        form.add_error(None, 'This account is not authorized as Teacher.')
                        return render(request, 'departments/teacher_login.html', {'form': form})
                    
                    # Login user
                    login(request, user)
                    
                    # Store session data
                    request.session['user_role'] = 'Teacher'
                    request.session['user_profile_id'] = profile.id
                    
                    # Redirect to teacher dashboard
                    return redirect('teacher_dashboard')
                    
                except UserProfile.DoesNotExist:
                    form.add_error(None, 'User profile not found. Please contact administrator.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = TeacherLoginForm()
    
    return render(request, 'departments/teacher_login.html', {'form': form})

@login_required
def dashboard_router(request):
    try:
        profile = request.user.userprofile
        # Route to appropriate dashboard based on role
        if profile.role == 'Principal':
            return redirect('principal_dashboard')
        elif profile.role == 'Vice Principal':
            return redirect('vice_principal_dashboard')
        elif profile.role == 'Chief of Works':
            return redirect('chief_of_works_dashboard')
        elif profile.role == 'Discipline Master':
            return redirect('discipline_master_dashboard')
        elif profile.role == 'Senior Discipline Master':
            return redirect('discipline_master_dashboard')
        elif profile.role == 'Secretary':
            return redirect('secretary_dashboard')
        elif profile.role == 'Accountant':
            return redirect('accountant_dashboard')
        elif profile.role == 'Teacher':
            return redirect('teacher_dashboard')
        else:
            return redirect('custom_admin_login')
    except UserProfile.DoesNotExist:
        return redirect('custom_admin_login')

# ==================== NEW DASHBOARD VIEWS ====================

@login_required
def principal_dashboard(request):
    # Check if user is authorized as Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Get counts for dashboard
    total_users = UserProfile.objects.count()
    total_departments = Department.objects.count()
    
    # Get actual data
    departments = Department.objects.all().prefetch_related('stream_set')
    users = UserProfile.objects.all().select_related('user', 'department')
    
    # Note: For classes and students, you'll need to integrate with your core app
    # For now, we'll use placeholders
    total_classes = 0
    total_students = 0
    
    # Prepare context for principal dashboard
    context = {
        'user': request.user,
        'user_profile': profile,
        'total_users': total_users,
        'total_departments': total_departments,
        'total_classes': total_classes,
        'total_students': total_students,
        'departments': departments,
        'users': users,
    }
    return render(request, 'departments/principal_dashboard.html', context)

@login_required
def vice_principal_dashboard(request):
    # Check if user is authorized as Vice Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Vice Principal':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Get stream password (for display purposes only)
    stream_password_display = "stream123" if hasattr(profile, 'stream_password') and profile.stream_password else "Not set"
    
    # Get statistics for the dashboard
    student_count = 42  # Example data - replace with actual query
    teacher_count = 8   # Example data
    attendance_rate = 94.5  # Example data
    pass_rate = 87.3  # Example data
    
    student_count_change = 3  # Example: +3 students since last week
    teacher_count_change = 1  # Example: +1 teacher
    attendance_change = 1.2  # Example: +1.2%
    pass_rate_change = 2.5  # Example: +2.5%
    
    # Recent activities
    recent_activities = [
        {
            'title': 'New Student Enrollment',
            'description': 'John Doe enrolled in Form 4A',
            'type': 'success',
            'icon': 'user-plus',
            'time': '2 hours ago'
        },
        {
            'title': 'Attendance Submitted',
            'description': 'Form 3B attendance for today',
            'type': 'info',
            'icon': 'clipboard-check',
            'time': '4 hours ago'
        },
        {
            'title': 'Exam Results Uploaded',
            'description': 'Mid-term exams for Mathematics',
            'type': 'warning',
            'icon': 'file-alt',
            'time': '1 day ago'
        }
    ]
    
    # Upcoming events
    upcoming_events = [
        {
            'name': 'Parent-Teacher Meeting',
            'description': 'Quarterly meeting with parents',
            'date': timezone.now() + timedelta(days=3)
        },
        {
            'name': 'Sports Day',
            'description': 'Annual inter-house sports competition',
            'date': timezone.now() + timedelta(days=7)
        },
        {
            'name': 'Term Exams',
            'description': 'End of term examinations',
            'date': timezone.now() + timedelta(days=14)
        }
    ]
    
    # Password last updated date
    password_last_updated = timezone.now() - timedelta(days=30)
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'stream_password': stream_password_display,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'attendance_rate': attendance_rate,
        'pass_rate': pass_rate,
        'student_count_change': student_count_change,
        'teacher_count_change': teacher_count_change,
        'attendance_change': attendance_change,
        'pass_rate_change': pass_rate_change,
        'recent_activities': recent_activities,
        'upcoming_events': upcoming_events,
        'password_last_updated': password_last_updated,
    }
    return render(request, 'departments/vice_principal_dashboard.html', context)

@login_required
def chief_of_works_dashboard(request):
    # Check if user is authorized as Chief of Works
    try:
        profile = request.user.userprofile
        if profile.role != 'Chief of Works':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Get department password (for display purposes only)
    department_password_display = "dept123" if hasattr(profile, 'department_password') and profile.department_password else "Not set"
    
    # Get department-specific statistics
    workshop_count = 5  # Example: 5 active workshops
    student_count = 65  # Example: 65 technical students
    equipment_count = 127  # Example: 127 equipment items
    maintenance_count = 8  # Example: 8 pending maintenance requests
    
    workshop_change = 1  # Example: +1 workshop this term
    student_change = 3  # Example: +3 students
    equipment_change = 5  # Example: +5 new equipment
    maintenance_change = 2  # Example: +2 urgent maintenance requests
    
    # Recent activities
    recent_activities = [
        {
            'title': 'Workshop Safety Inspection',
            'description': 'Monthly safety check completed',
            'type': 'info',
            'icon': 'shield-alt',
            'time': 'Yesterday',
            'workshop': 'Mechanical Workshop'
        },
        {
            'title': 'Equipment Maintenance',
            'description': 'Drill machine serviced',
            'type': 'warning',
            'icon': 'wrench',
            'time': '2 days ago',
            'workshop': 'Electrical Workshop'
        },
        {
            'title': 'New Equipment Received',
            'description': '5 new multimeters delivered',
            'type': 'success',
            'icon': 'box-open',
            'time': '3 days ago',
            'workshop': 'All Workshops'
        }
    ]
    
    # Equipment status
    functional_count = 95  # Example: 95 functional items
    repair_count = 12  # Example: 12 items need repair
    loaned_count = 20  # Example: 20 items currently loaned
    
    # Utilization and compliance rates
    utilization_rate = 78  # Example: 78% utilization
    compliance_rate = 92  # Example: 92% maintenance compliance
    
    # Last security audit date
    last_audit = timezone.now() - timedelta(days=15)
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'department_password': department_password_display,
        'workshop_count': workshop_count,
        'student_count': student_count,
        'equipment_count': equipment_count,
        'maintenance_count': maintenance_count,
        'workshop_change': workshop_change,
        'student_change': student_change,
        'equipment_change': equipment_change,
        'maintenance_change': maintenance_change,
        'recent_activities': recent_activities,
        'functional_count': functional_count,
        'repair_count': repair_count,
        'loaned_count': loaned_count,
        'utilization_rate': utilization_rate,
        'compliance_rate': compliance_rate,
        'last_audit': last_audit,
    }
    return render(request, 'departments/chief_of_works_dashboard.html', context)

@login_required
def discipline_master_dashboard(request):
    # Check if user is authorized as Discipline Master or Senior Discipline Master
    try:
        profile = request.user.userprofile
        if profile.role not in ['Discipline Master', 'Senior Discipline Master']:
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Get floor password if available (for display purposes only)
    floor_password_display = "floor123" if hasattr(profile, 'floor_password') and profile.floor_password else "Not required"
    
    # Discipline statistics
    incident_count = 3  # Example: 3 incidents today
    late_count = 12  # Example: 12 late arrivals
    compliance_rate = 92  # Example: 92% uniform compliance
    positive_count = 5  # Example: 5 positive behaviors recorded
    
    incident_change = 1  # Example: +1 incident
    late_change = -2  # Example: -2 late arrivals (improvement)
    compliance_change = 1.5  # Example: +1.5% compliance
    positive_change = 2  # Example: +2 positive behaviors
    
    # Recent incidents
    recent_incidents = [
        {
            'id': 101,
            'student': 'John Smith',
            'class': 'Form 4B',
            'type': 'Disruptive Behavior',
            'type_color': 'danger',
            'floor': 'Middle Floor',
            'status': 'Pending Review',
            'status_color': 'warning',
            'time': '10:30 AM'
        },
        {
            'id': 102,
            'student': 'Mary Johnson',
            'class': 'Form 3A',
            'type': 'Uniform Violation',
            'type_color': 'warning',
            'floor': 'Down Floor',
            'status': 'Resolved',
            'status_color': 'success',
            'time': '9:15 AM'
        },
        {
            'id': 103,
            'student': 'David Wilson',
            'class': 'Form 5C',
            'type': 'Late Arrival',
            'type_color': 'info',
            'floor': 'Top Floor',
            'status': 'Warning Issued',
            'status_color': 'primary',
            'time': '8:00 AM'
        }
    ]
    
    # Floor status
    floor_status = [
        {
            'name': 'Down Floor',
            'status': 'All Clear',
            'status_color': 'success'
        },
        {
            'name': 'Middle Floor',
            'status': 'Active Monitoring',
            'status_color': 'warning'
        },
        {
            'name': 'Top Floor',
            'status': 'All Clear',
            'status_color': 'success'
        }
    ]
    
    # If Senior Discipline Master, add additional data
    senior_tools = profile.role == 'Senior Discipline Master'
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'floor_password': floor_password_display,
        'incident_count': incident_count,
        'late_count': late_count,
        'compliance_rate': compliance_rate,
        'positive_count': positive_count,
        'incident_change': incident_change,
        'late_change': late_change,
        'compliance_change': compliance_change,
        'positive_change': positive_change,
        'recent_incidents': recent_incidents,
        'floor_status': floor_status,
        'senior_tools': senior_tools,
    }
    return render(request, 'departments/discipline_master_dashboard.html', context)

@login_required
def secretary_dashboard(request):
    # Check if user is authorized as Secretary
    try:
        profile = request.user.userprofile
        if profile.role != 'Secretary':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Office statistics
    pending_documents = 8  # Example: 8 pending documents
    unread_messages = 12  # Example: 12 unread messages
    upcoming_meetings = 3  # Example: 3 upcoming meetings
    urgent_tasks = 2  # Example: 2 urgent tasks
    
    document_change = 2  # Example: +2 documents
    message_change = 3  # Example: +3 messages
    meeting_change = 1  # Example: +1 meeting
    task_change = -1  # Example: -1 task (completed)
    
    # Recent activities
    recent_activities = [
        {
            'title': 'Official Letter Typed',
            'description': 'Letter to Ministry of Education',
            'category': 'Document',
            'category_color': 'primary',
            'priority': 'High',
            'priority_color': 'danger',
            'status': 'For Signing',
            'status_color': 'warning',
            'time': 'Today, 10:00 AM'
        },
        {
            'title': 'Meeting Scheduled',
            'description': 'Parent-Teacher Association meeting',
            'category': 'Scheduling',
            'category_color': 'success',
            'priority': 'Medium',
            'priority_color': 'warning',
            'status': 'Confirmed',
            'status_color': 'success',
            'time': 'Yesterday, 3:30 PM'
        },
        {
            'title': 'Visitor Logged',
            'description': 'Supplier delivery - ABC Supplies',
            'category': 'Visitor',
            'category_color': 'info',
            'priority': 'Low',
            'priority_color': 'success',
            'status': 'Completed',
            'status_color': 'success',
            'time': 'Yesterday, 11:15 AM'
        }
    ]
    
    # Today's schedule
    todays_schedule = [
        {
            'time': '9:00 AM',
            'title': 'Morning Briefing',
            'description': 'Daily staff briefing with Principal',
            'type': 'Meeting',
            'type_color': 'primary',
            'location': 'Principal Office'
        },
        {
            'time': '11:00 AM',
            'title': 'Document Filing',
            'description': 'Weekly document organization',
            'type': 'Task',
            'type_color': 'info',
            'location': 'Records Room'
        },
        {
            'time': '2:00 PM',
            'title': 'Parent Meeting',
            'description': 'Meeting with Mr. Johnson (Form 4B parent)',
            'type': 'Appointment',
            'type_color': 'success',
            'location': 'Reception'
        }
    ]
    
    # Document queue breakdown
    for_review = 3  # Example: 3 documents for review
    for_signing = 4  # Example: 4 documents for signing
    for_filing = 1  # Example: 1 document for filing
    
    # Recent documents
    recent_documents = [
        {
            'id': 'DOC-2024-001',
            'title': 'Staff Meeting Minutes',
            'description': 'Minutes from last staff meeting',
            'submitter': 'Mr. Anderson',
            'date': 'Today',
            'status': 'For Review',
            'status_color': 'warning'
        },
        {
            'id': 'DOC-2024-002',
            'title': 'Budget Request Form',
            'description': 'Request for laboratory equipment',
            'submitter': 'Science Department',
            'date': 'Yesterday',
            'status': 'For Signing',
            'status_color': 'info'
        },
        {
            'id': 'DOC-2024-003',
            'title': 'Visitor Report',
            'description': 'Monthly visitor statistics',
            'submitter': 'Security',
            'date': '2 days ago',
            'status': 'For Filing',
            'status_color': 'success'
        }
    ]
    
    # Today's date
    today = timezone.now()
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'pending_documents': pending_documents,
        'unread_messages': unread_messages,
        'upcoming_meetings': upcoming_meetings,
        'urgent_tasks': urgent_tasks,
        'document_change': document_change,
        'message_change': message_change,
        'meeting_change': meeting_change,
        'task_change': task_change,
        'recent_activities': recent_activities,
        'todays_schedule': todays_schedule,
        'today': today,
        'for_review': for_review,
        'for_signing': for_signing,
        'for_filing': for_filing,
        'recent_documents': recent_documents,
    }
    return render(request, 'departments/secretary_dashboard.html', context)

@login_required
def accountant_dashboard(request):
    # Check if user is authorized as Accountant
    try:
        profile = request.user.userprofile
        if profile.role != 'Accountant':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Financial statistics
    total_revenue = 152500.75  # Example: $152,500.75
    total_expenses = 98750.25  # Example: $98,750.25
    pending_invoices = 15  # Example: 15 pending invoices
    collection_rate = 87.5  # Example: 87.5% collection rate
    
    revenue_change = 5.2  # Example: +5.2%
    expense_change = 3.1  # Example: +3.1%
    invoice_change = 2  # Example: +2 invoices
    collection_change = 1.8  # Example: +1.8%
    
    # Financial breakdown
    tuition_fees = 125000.00
    exam_fees = 17500.00
    other_fees = 10000.75
    
    salary_expenses = 75000.00
    utility_expenses = 12500.25
    supply_expenses = 11250.00
    
    # Calculate percentages
    total_income = tuition_fees + exam_fees + other_fees
    total_expense = salary_expenses + utility_expenses + supply_expenses
    
    tuition_percent = (tuition_fees / total_income * 100) if total_income > 0 else 0
    exam_percent = (exam_fees / total_income * 100) if total_income > 0 else 0
    other_percent = (other_fees / total_income * 100) if total_income > 0 else 0
    
    salary_percent = (salary_expenses / total_expense * 100) if total_expense > 0 else 0
    utility_percent = (utility_expenses / total_expense * 100) if total_expense > 0 else 0
    supply_percent = (supply_expenses / total_expense * 100) if total_expense > 0 else 0
    
    # Net profit/loss
    net_profit = total_revenue - total_expenses
    
    # Recent transactions
    recent_transactions = [
        {
            'id': 'TXN-2024-001',
            'date': 'Today',
            'description': 'Tuition Fee Payment',
            'payer': 'John Doe (Form 4B)',
            'amount': 250.00,
            'type': 'income',
            'status': 'Completed',
            'status_color': 'success'
        },
        {
            'id': 'TXN-2024-002',
            'date': 'Yesterday',
            'description': 'Utility Bill Payment',
            'payer': 'Electricity Company',
            'amount': 1250.75,
            'type': 'expense',
            'status': 'Paid',
            'status_color': 'success'
        },
        {
            'id': 'TXN-2024-003',
            'date': '2 days ago',
            'description': 'Examination Fees',
            'payer': 'Mary Johnson (Form 3A)',
            'amount': 75.00,
            'type': 'income',
            'status': 'Pending',
            'status_color': 'warning'
        }
    ]
    
    # Fee collection status
    paid_percent = 65  # Example: 65% paid
    partial_percent = 15  # Example: 15% partial
    unpaid_percent = 20  # Example: 20% unpaid
    
    # Upcoming payments
    upcoming_payments = [
        {
            'id': 'PAY-001',
            'title': 'Teacher Salary',
            'description': 'Monthly salary disbursement',
            'amount': 45000.00,
            'days_left': 5,
            'priority': 'high'
        },
        {
            'id': 'PAY-002',
            'title': 'Internet Bill',
            'description': 'Quarterly internet subscription',
            'amount': 1200.00,
            'days_left': 10,
            'priority': 'medium'
        },
        {
            'id': 'PAY-003',
            'title': 'Lab Equipment',
            'description': 'Science lab equipment order',
            'amount': 7500.00,
            'days_left': 15,
            'priority': 'medium'
        }
    ]
    
    upcoming_count = len(upcoming_payments)
    fiscal_year = timezone.now().year
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'pending_invoices': pending_invoices,
        'collection_rate': collection_rate,
        'revenue_change': revenue_change,
        'expense_change': expense_change,
        'invoice_change': invoice_change,
        'collection_change': collection_change,
        'tuition_fees': tuition_fees,
        'exam_fees': exam_fees,
        'other_fees': other_fees,
        'salary_expenses': salary_expenses,
        'utility_expenses': utility_expenses,
        'supply_expenses': supply_expenses,
        'tuition_percent': tuition_percent,
        'exam_percent': exam_percent,
        'other_percent': other_percent,
        'salary_percent': salary_percent,
        'utility_percent': utility_percent,
        'supply_percent': supply_percent,
        'net_profit': net_profit,
        'recent_transactions': recent_transactions,
        'paid_percent': paid_percent,
        'partial_percent': partial_percent,
        'unpaid_percent': unpaid_percent,
        'upcoming_payments': upcoming_payments,
        'upcoming_count': upcoming_count,
        'fiscal_year': fiscal_year,
    }
    return render(request, 'departments/accountant_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    # Check if user is authorized as Teacher
    try:
        profile = request.user.userprofile
        if profile.role != 'Teacher':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Get assigned classes for the teacher (using dummy data)
    assigned_classes = [
        {'id': 1, 'name': 'Form 4B', 'subject': 'Mathematics', 'student_count': 38, 'schedule': 'Mon, Wed, Fri 8:00 AM', 'average_grade': 85.5, 'room': 'Room 401'},
        {'id': 2, 'name': 'Form 3A', 'subject': 'Mathematics', 'student_count': 36, 'schedule': 'Tue, Thu 9:15 AM', 'average_grade': 78.2, 'room': 'Room 302'},
        {'id': 3, 'name': 'Form 2C', 'subject': 'Mathematics', 'student_count': 35, 'schedule': 'Mon, Wed 10:30 AM', 'average_grade': 82.7, 'room': 'Room 203'},
        {'id': 4, 'name': 'Form 1A', 'subject': 'Mathematics', 'student_count': 36, 'schedule': 'Tue, Thu 2:00 PM', 'average_grade': 88.1, 'room': 'Room 104'},
    ]
    
    # Teacher statistics
    total_students = sum([c['student_count'] for c in assigned_classes])
    pending_assignments = 8  # Example: 8 pending assignments to grade
    upcoming_exams = 3  # Example: 3 upcoming exams
    unread_messages = 5  # Example: 5 unread messages
    
    assignment_change = 2  # Example: +2 assignments
    exam_change = 1  # Example: +1 exam
    message_change = 1  # Example: +1 message
    
    # Today's schedule (simplified - would normally check actual schedule)
    todays_schedule = [
        {
            'id': 1,
            'name': 'Form 4B - Mathematics',
            'subject': 'Mathematics',
            'student_count': 38,
            'time': '8:00 AM - 9:30 AM',
            'room': 'Room 401',
            'status': 'completed'
        },
        {
            'id': 2,
            'name': 'Form 3A - Mathematics',
            'subject': 'Mathematics',
            'student_count': 36,
            'time': '10:30 AM - 12:00 PM',
            'room': 'Room 302',
            'status': 'upcoming'
        },
        {
            'id': 4,
            'name': 'Form 1A - Mathematics',
            'subject': 'Mathematics',
            'student_count': 36,
            'time': '2:00 PM - 3:30 PM',
            'room': 'Room 104',
            'status': 'upcoming'
        }
    ]
    
    # Upcoming deadlines
    upcoming_deadlines = [
        {
            'title': 'Grade Assignment 1',
            'days_left': 2,
            'priority_color': 'danger',
            'percent': 25
        },
        {
            'title': 'Submit Exam Questions',
            'days_left': 5,
            'priority_color': 'warning',
            'percent': 50
        },
        {
            'title': 'Parent Meeting Prep',
            'days_left': 7,
            'priority_color': 'info',
            'percent': 75
        }
    ]
    
    # Recent student activities
    recent_activities = [
        {
            'student': 'John Smith',
            'description': 'Submitted Assignment 3',
            'type_color': 'success',
            'icon': 'file-upload',
            'class': 'Form 4B',
            'time': '2 hours ago'
        },
        {
            'student': 'Mary Johnson',
            'description': 'Asked question about Algebra',
            'type_color': 'info',
            'icon': 'question-circle',
            'class': 'Form 3A',
            'time': '4 hours ago'
        },
        {
            'student': 'David Wilson',
            'description': 'Improved grade from C to B',
            'type_color': 'warning',
            'icon': 'chart-line',
            'class': 'Form 2C',
            'time': '1 day ago'
        }
    ]
    
    # Teaching resources counts
    lesson_plan_count = 15  # Example: 15 lesson plans available
    presentation_count = 8  # Example: 8 presentations
    video_count = 12  # Example: 12 videos
    worksheet_count = 20  # Example: 20 worksheets
    
    # Today's date
    today = timezone.now()
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'assigned_classes': assigned_classes,
        'total_students': total_students,
        'pending_assignments': pending_assignments,
        'upcoming_exams': upcoming_exams,
        'unread_messages': unread_messages,
        'assignment_change': assignment_change,
        'exam_change': exam_change,
        'message_change': message_change,
        'todays_schedule': todays_schedule,
        'today': today,
        'upcoming_deadlines': upcoming_deadlines,
        'recent_activities': recent_activities,
        'lesson_plan_count': lesson_plan_count,
        'presentation_count': presentation_count,
        'video_count': video_count,
        'worksheet_count': worksheet_count,
    }
    return render(request, 'departments/teacher_dashboard.html', context)

# ==================== SETUP VIEWS (For Principal Dashboard) ====================

@login_required
def create_initial_departments(request):
    """View to create initial departments when system is first set up"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    # Define the 3 main departments
    departments_to_create = [
        {'name': 'General Department', 'code': 'GEN'},
        {'name': 'Industrial Department', 'code': 'IND'},
        {'name': 'Commercial Department', 'code': 'COM'},
    ]
    
    created_departments = []
    for dept_data in departments_to_create:
        # Create department if it doesn't exist
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'code': dept_data['code']}
        )
        if created:
            created_departments.append(dept_data['name'])
            
            # Create streams for each department
            Stream.objects.get_or_create(
                name='first_cycle',
                department=dept,
                defaults={'name': 'first_cycle'}
            )
            Stream.objects.get_or_create(
                name='second_cycle',
                department=dept,
                defaults={'name': 'second_cycle'}
            )
    
    # Create floors if they don't exist
    floors_to_create = [
        {'name': 'down', 'description': 'Down Floor'},
        {'name': 'middle', 'description': 'Middle Floor'},
        {'name': 'top', 'description': 'Top Floor'},
    ]
    
    created_floors = []
    for floor_data in floors_to_create:
        floor, created = Floor.objects.get_or_create(
            name=floor_data['name'],
            defaults={'description': floor_data['description']}
        )
        if created:
            created_floors.append(floor_data['description'])
    
    # Prepare success message
    if created_departments:
        messages.success(request, f'Successfully created departments: {", ".join(created_departments)}')
    else:
        messages.info(request, 'All departments already exist.')
    
    if created_floors:
        messages.success(request, f'Successfully created floors: {", ".join(created_floors)}')
    
    return redirect('principal_dashboard')

@login_required
def create_department_view(request):
    """View for creating a single department (quick create)"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    if request.method == 'POST':
        form = DepartmentCreationForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department "{department.name}" created successfully!')
            return redirect('principal_dashboard')
    else:
        form = DepartmentCreationForm()
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'form': form,
        'form_title': 'Create New Department',
        'submit_label': 'Create Department',
        'back_url': 'principal_dashboard',
    }
    return render(request, 'departments/form_template.html', context)

@login_required
def edit_department(request, department_id):
    """View for editing a department"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            messages.error(request, 'Only Principal can edit departments.')
            return redirect('principal_dashboard')
    except:
        return redirect('unauthorized')
    
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        form = DepartmentEditForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department "{department.name}" updated successfully!')
            return redirect('principal_dashboard')
    else:
        form = DepartmentEditForm(instance=department)
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'form': form,
        'form_title': f'Edit Department: {department.name}',
        'submit_label': 'Update Department',
        'back_url': 'principal_dashboard',
    }
    return render(request, 'departments/form_template.html', context)

@login_required
def delete_department(request, department_id):
    """View for deleting a department"""
    # Check if user is Principal (only Principal should delete departments)
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            messages.error(request, 'Only Principal can delete departments.')
            return redirect('principal_dashboard')
    except:
        return redirect('unauthorized')
    
    try:
        # Get the department to delete
        department = Department.objects.get(id=department_id)
        department_name = department.name
        
        # Check if department has users assigned (optional safety check)
        if UserProfile.objects.filter(department=department).exists():
            messages.error(request, f'Cannot delete "{department_name}" because it has users assigned. Reassign users first.')
            return redirect('principal_dashboard')
        
        # Delete the department
        department.delete()
        messages.success(request, f'Department "{department_name}" deleted successfully!')
        
    except Department.DoesNotExist:
        messages.error(request, 'Department not found.')
    except Exception as e:
        messages.error(request, f'Error deleting department: {str(e)}')
    
    return redirect('principal_dashboard')

@login_required
def create_user_view(request):
    """View for creating a new user (quick create)"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request=request)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created successfully with role "{form.cleaned_data["role"]}"!')
            return redirect('principal_dashboard')
    else:
        form = UserCreationForm(request=request)
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'form': form,
        'form_title': 'Create New User',
        'submit_label': 'Create User',
        'back_url': 'principal_dashboard',
    }
    return render(request, 'departments/form_template.html', context)

@login_required
def edit_user(request, user_id):
    """View for editing a user"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            messages.error(request, 'Only Principal can edit users.')
            return redirect('principal_dashboard')
    except:
        return redirect('unauthorized')
    
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user, user_profile_instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user.username}" updated successfully!')
            return redirect('principal_dashboard')
    else:
        form = UserEditForm(instance=user, user_profile_instance=user_profile)
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'form': form,
        'form_title': f'Edit User: {user.username}',
        'submit_label': 'Update User',
        'back_url': 'principal_dashboard',
    }
    return render(request, 'departments/form_template.html', context)

@login_required
def delete_user(request, user_id):
    """View for deleting a user"""
    # Check if user is Principal (only Principal should delete users)
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            messages.error(request, 'Only Principal can delete users.')
            return redirect('principal_dashboard')
    except:
        return redirect('unauthorized')
    
    try:
        # Get the user to delete
        user = User.objects.get(id=user_id)
        username = user.username
        
        # Prevent deletion of self
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('principal_dashboard')
        
        # Delete the user (this will cascade delete UserProfile due to CASCADE)
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
        
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('principal_dashboard')

@login_required
def reset_password(request, user_id):
    """View for resetting a user's password with copy/edit functionality"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            messages.error(request, 'Only Principal can reset passwords.')
            return redirect('principal_dashboard')
    except:
        return redirect('unauthorized')
    
    try:
        # Get the user
        user = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            # Handle form submission
            if 'generate_password' in request.POST:
                # Generate a new random password
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                return render(request, 'departments/reset_password_form.html', {
                    'user': request.user,
                    'user_profile': profile,
                    'target_user': user,
                    'temp_password': temp_password,
                    'form_title': f'Reset Password for {user.username}',
                    'submit_label': 'Set New Password',
                    'back_url': 'principal_dashboard',
                })
            
            elif 'set_password' in request.POST:
                # Set the new password
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                if not new_password or not confirm_password:
                    messages.error(request, 'Both password fields are required.')
                    return render(request, 'departments/reset_password_form.html', {
                        'user': request.user,
                        'user_profile': profile,
                        'target_user': user,
                        'temp_password': new_password or '',
                        'form_title': f'Reset Password for {user.username}',
                        'submit_label': 'Set New Password',
                        'back_url': 'principal_dashboard',
                    })
                
                if new_password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'departments/reset_password_form.html', {
                        'user': request.user,
                        'user_profile': profile,
                        'target_user': user,
                        'temp_password': new_password,
                        'form_title': f'Reset Password for {user.username}',
                        'submit_label': 'Set New Password',
                        'back_url': 'principal_dashboard',
                    })
                
                # Set the new password
                user.set_password(new_password)
                user.save()
                
                # Log the action
                messages.success(request, f'Password for "{user.username}" has been reset successfully!')
                return redirect('principal_dashboard')
        
        else:
            # GET request - show form with generated password
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            return render(request, 'departments/reset_password_form.html', {
                'user': request.user,
                'user_profile': profile,
                'target_user': user,
                'temp_password': temp_password,
                'form_title': f'Reset Password for {user.username}',
                'submit_label': 'Set New Password',
                'back_url': 'principal_dashboard',
            })
        
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('principal_dashboard')
    except Exception as e:
        messages.error(request, f'Error resetting password: {str(e)}')
        return redirect('principal_dashboard')

@login_required
def create_class_view(request):
    """View for creating a new class (quick create)"""
    # Check if user is Principal
    try:
        profile = request.user.userprofile
        if profile.role != 'Principal':
            return redirect('unauthorized')
    except:
        return redirect('unauthorized')
    
    if request.method == 'POST':
        form = ClassCreationForm(request.POST)
        if form.is_valid():
            # Note: This is a simplified form. In production, you'd create actual Class objects
            # For now, we'll just show a success message
            class_name = form.cleaned_data['name']
            messages.success(request, f'Class "{class_name}" would be created here (integration with core app needed).')
            return redirect('principal_dashboard')
    else:
        form = ClassCreationForm()
    
    context = {
        'user': request.user,
        'user_profile': profile,
        'form': form,
        'form_title': 'Create New Class',
        'submit_label': 'Create Class',
        'back_url': 'principal_dashboard',
    }
    return render(request, 'departments/form_template.html', context)

# ==================== DASHBOARD FORM HANDLERS ====================

# These are placeholder views for form submissions in the dashboards
# You should implement proper form handling for each of these

@login_required
def request_stream_change(request):
    """Handle stream change requests from Vice Principal"""
    if request.method == 'POST':
        # Process the stream change request
        requested_stream = request.POST.get('requested_stream')
        reason = request.POST.get('reason')
        
        # Here you would save the request to database and notify Principal
        # For now, just show a success message
        messages.success(request, 'Stream change request submitted successfully! The Principal will review it.')
    
    return redirect('vice_principal_dashboard')

@login_required
def request_password_change(request):
    """Handle password change requests"""
    if request.method == 'POST':
        # Process password change request
        reason = request.POST.get('reason')
        
        # Here you would save the request to database
        messages.success(request, 'Password change request submitted! The Principal will review it.')
    
    return redirect('vice_principal_dashboard')

@login_required
def send_parent_announcement(request):
    """Handle parent announcement from Vice Principal"""
    if request.method == 'POST':
        # Process announcement
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Here you would save and send the announcement
        messages.success(request, 'Announcement sent to parents successfully!')
    
    return redirect('vice_principal_dashboard')

@login_required
def update_department_settings(request):
    """Handle department settings update from Chief of Works"""
    if request.method == 'POST':
        # Process settings update
        workshop_hours = request.POST.get('workshop_hours')
        
        # Here you would save the settings
        messages.success(request, 'Department settings updated successfully!')
    
    return redirect('chief_of_works_dashboard')

@login_required
def schedule_workshop(request):
    """Handle workshop scheduling from Chief of Works"""
    if request.method == 'POST':
        # Process workshop scheduling
        title = request.POST.get('title')
        date = request.POST.get('date')
        
        # Here you would save the workshop schedule
        messages.success(request, f'Workshop "{title}" scheduled successfully!')
    
    return redirect('chief_of_works_dashboard')

@login_required
def request_department_password_change(request):
    """Handle department password change requests from Chief of Works"""
    if request.method == 'POST':
        # Process password change request
        reason = request.POST.get('reason')
        
        # Here you would save the request
        messages.success(request, 'Department password change request submitted!')
    
    return redirect('chief_of_works_dashboard')

@login_required
def report_incident(request):
    """Handle incident reporting from Discipline Master"""
    if request.method == 'POST':
        # Process incident report
        student = request.POST.get('student')
        incident_type = request.POST.get('type')
        
        # Here you would save the incident
        messages.success(request, f'Incident reported for {student} successfully!')
    
    return redirect('discipline_master_dashboard')

@login_required
def record_positive_behavior(request):
    """Handle positive behavior recording from Discipline Master"""
    if request.method == 'POST':
        # Process positive behavior
        student = request.POST.get('student')
        behavior = request.POST.get('behavior')
        
        # Here you would save the positive behavior
        messages.success(request, f'Positive behavior recorded for {student}!')
    
    return redirect('discipline_master_dashboard')

@login_required
def upload_document(request):
    """Handle document upload from Secretary"""
    if request.method == 'POST':
        # Process document upload
        title = request.POST.get('title')
        
        # Here you would save the uploaded document
        messages.success(request, f'Document "{title}" uploaded successfully!')
    
    return redirect('secretary_dashboard')

@login_required
def record_payment(request):
    """Handle payment recording from Accountant"""
    if request.method == 'POST':
        # Process payment
        payer = request.POST.get('payer')
        amount = request.POST.get('amount')
        
        # Here you would save the payment
        messages.success(request, f'Payment of ${amount} from {payer} recorded successfully!')
    
    return redirect('accountant_dashboard')

@login_required
def create_lesson_plan(request):
    """Handle lesson plan creation from Teacher"""
    if request.method == 'POST':
        # Process lesson plan
        topic = request.POST.get('topic')
        class_id = request.POST.get('class_id')
        
        # Here you would save the lesson plan
        messages.success(request, f'Lesson plan for "{topic}" created successfully!')
    
    return redirect('teacher_dashboard')

# ==================== LEGACY DASHBOARD VIEWS (For backward compatibility) ====================

@login_required
def general_dashboard(request):
    # Legacy view - redirect to vice_principal_dashboard if user is Vice Principal
    try:
        profile = request.user.userprofile
        if profile.role == 'Vice Principal':
            return redirect('vice_principal_dashboard')
    except:
        pass
    
    return redirect('unauthorized')

@login_required
def industrial_dashboard(request):
    # Legacy view - redirect to chief_of_works_dashboard if user is Chief of Works
    try:
        profile = request.user.userprofile
        if profile.role == 'Chief of Works' and profile.department.name == "Industrial":
            return redirect('chief_of_works_dashboard')
    except:
        pass
    
    return redirect('unauthorized')

@login_required
def commercial_dashboard(request):
    # Legacy view - redirect to chief_of_works_dashboard if user is Chief of Works
    try:
        profile = request.user.userprofile
        if profile.role == 'Chief of Works' and profile.department.name == "Commercial":
            return redirect('chief_of_works_dashboard')
    except:
        pass
    
    return redirect('unauthorized')

@login_required
def discipline_dashboard(request):
    # Legacy view - redirect to discipline_master_dashboard
    try:
        profile = request.user.userprofile
        if profile.role == 'Discipline Master':
            return redirect('discipline_master_dashboard')
    except:
        pass
    
    return redirect('unauthorized')

@login_required
def senior_discipline_dashboard(request):
    # Legacy view - redirect to discipline_master_dashboard
    try:
        profile = request.user.userprofile
        if profile.role == 'Senior Discipline Master':
            return redirect('discipline_master_dashboard')
    except:
        pass
    
    return redirect('unauthorized')

@login_required
def admin_dashboard(request):
    # Legacy view - for superusers only
    if not request.user.is_superuser:
        return redirect('unauthorized')
    
    return render(request, 'departments/admin_dashboard.html', {
        'user': request.user
    })

def unauthorized(request):
    return render(request, 'departments/unauthorized.html')

def home_page(request):
    return render(request, 'departments/home_page.html')

def custom_logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def chat_room(request):
    # Fetch all users except the currently logged-in one
    users = User.objects.exclude(id=request.user.id).select_related('status', 'userprofile')
    
    # Get all messages where the current user is either the sender OR the receiver
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'departments/chat.html', {
        'users': users, 
        'messages': messages
    })

@login_required
def private_chat(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    # 1. Fetch the last 50 messages between these two users
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=target_user)) |
        (Q(sender=target_user) & Q(receiver=request.user))
    ).order_by('timestamp')[:50]

    # 2. Mark any unread messages FROM the other person TO me as "Read"
    Message.objects.filter(sender=target_user, receiver=request.user, is_read=False).update(is_read=True)

    return render(request, 'departments/private_messages.html', {
        'target_user': target_user,
        'chat_messages': messages  # Send the history to the template
    })

@csrf_exempt
@login_required
def upload_chat_file(request):
    if request.method == 'POST' and (request.FILES.get('image') or request.FILES.get('file')):
        # Get the uploaded file
        uploaded_file = request.FILES.get('image') or request.FILES.get('file')
        
        # Generate a unique filename to avoid overwrites
        import uuid
        import os
        file_extension = os.path.splitext(uploaded_file.name)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save it to a 'chat_uploads' folder in your media directory
        file_path = f'chat_uploads/{unique_filename}'
        saved_path = default_storage.save(file_path, uploaded_file)
        file_url = default_storage.url(saved_path)
        
        # Return the URL so the JavaScript can send it as a message
        return JsonResponse({
            'url': file_url, 
            'name': uploaded_file.name,
            'type': 'image' if 'image' in request.FILES else 'file'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def chat_list(request):  # <--- Make sure this is 'chat_list'
    # Get all users except the logged-in user
    users = User.objects.exclude(id=request.user.id)
    
    # Get the status for each user
    for user in users:
        UserStatus.objects.get_or_create(user=user)
        
    return render(request, 'departments/chat.html', {'users': users})
@login_required
def staff_chat_dashboard(request):
    """
    This view renders the main large-screen chat interface.
    """
    return render(request, 'departments/staff_chat.html')