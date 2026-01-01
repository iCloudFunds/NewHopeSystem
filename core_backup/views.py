from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, ModuleControl, DisciplineRecord, FeePayment, ParentLoginLog

def parent_login(request):
    """
    Handles parent authentication using Student Name and Admission Number.
    Records a security log on every successful entry.
    """
    # 1. Check if Superadmin has enabled the portal via ModuleControl
    portal_status = ModuleControl.objects.filter(module_name='PARENT_PORTAL', is_active=True).exists()
    
    if not portal_status:
        # If disabled, show the "Closed" page
        return render(request, 'core/portal_disabled.html')

    if request.method == 'POST':
        name = request.POST.get('full_name')
        admission = request.POST.get('admission_number')
        
        try:
            # 2. Validate credentials against the Student database
            student = Student.objects.get(
                full_name__iexact=name, 
                admission_number__iexact=admission
            )
            
            # 3. SECURITY LOG: Record who, when, and from where
            ParentLoginLog.objects.create(
                student=student,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            # 4. Create a session for the parent (valid for this student only)
            request.session['parent_student_id'] = student.id
            return redirect('parent_dashboard')
            
        except Student.DoesNotExist:
            messages.error(request, "Invalid Student Name or Admission Number")
            
    return render(request, 'core/parent_login.html')


def parent_dashboard(request):
    """
    Displays protected student data (Fees and Discipline) to the parent.
    Includes session-based security check.
    """
    # 1. Ensure the parent has a valid session
    student_id = request.session.get('parent_student_id')
    if not student_id:
        return redirect('parent_login')

    # 2. Fetch student data
    student = get_object_or_404(Student, id=student_id)
    
    # 3. Calculate Financial Balance from the most recent payment
    latest_payment = FeePayment.objects.filter(student=student).order_by('-date_of_payment').first()
    balance = latest_payment.balance if latest_payment else 0

    # 4. Fetch Discipline History
    discipline_records = DisciplineRecord.objects.filter(student=student).order_by('-incident_date')
    
    # 5. Calculate Conduct Score (Starts at 100, drops with infractions)
    total_deducted = sum(r.points_deducted for r in discipline_records)
    conduct_points = 100 - total_deducted

    # 6. Render the Secure (View-Only) Dashboard
    context = {
        'student': student,
        'balance': balance,
        'discipline_records': discipline_records,
        'conduct_points': conduct_points,
    }
    return render(request, 'core/parent_dashboard.html', context)