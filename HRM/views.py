from django.shortcuts import render, redirect, get_object_or_404
from .models import Department
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from employees.models import Employee
from core.models import PaymentMode,EmployeePaymentType
from django.core.paginator import Paginator
'''
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department.html', {'Departments': departments})
'''
@login_required
def department_list(request):
    departments = Department.objects.all()
    paginator = Paginator(departments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'department.html', {'page_obj': page_obj})

@login_required
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Department.objects.create(
            department_name=name,
            created_by=request.user,
            created_at=timezone.now()
        )
        return redirect('department_list')
    return render(request, 'add_department.html')

@login_required
def delete_department(request, sno):
    department = get_object_or_404(Department, sno=sno)
    department.delete()
    return redirect('department_list')

@login_required
def edit_department(request, sno):
    department = get_object_or_404(Department, sno=sno)
    if request.method == 'POST':
        department.department_name = request.POST.get('name')
        department.save()
        return redirect('department_list')
    return render(request, 'edit_department.html', {'department': department})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Empdata
from .forms import UserForm

@login_required
def user_list(request):
    users = Empdata.objects.all()
    return render(request, 'user_list1.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(Empdata, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(Empdata, pk=pk)
    user.delete()
    return redirect('user_list')


from django.shortcuts import render, get_object_or_404, redirect
from .models import EmployeePayment
from .forms import EmployeePaymentForm
from django.contrib import messages


from django.db.models import Sum
from collections import defaultdict
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.http import JsonResponse, HttpResponse
import csv

from HRM.models import EmployeePayment


@login_required
def employee_payment_dashboard(request):
    by_department = EmployeePayment.objects.values('department__department_name') \
        .annotate(total=Sum('amount'))

    by_method = EmployeePayment.objects.values('payment_method__name') \
        .annotate(total=Sum('amount'))

    by_type = EmployeePayment.objects.values('type__name') \
        .annotate(total=Sum('amount'))

    context = {
        'by_department': by_department,
        'by_method': by_method,
        'by_type': by_type,
    }
    return render(request, 'employee_payment_dashboard.html', context)


@login_required
def employee_payment_chart_data(request):
    filter = request.GET.get('filter', 'monthly')
    today = now().date()

    if filter == 'daily':
        dates = [today - timedelta(days=i) for i in reversed(range(7))]
        labels = [d.strftime('%d %b') for d in dates]
    elif filter == 'yearly':
        dates = [datetime(today.year - i, 1, 1).date() for i in reversed(range(3))]
        labels = [d.strftime('%Y') for d in dates]
    else:  # monthly
        dates = [datetime(today.year, i, 1).date() for i in range(1, 13)]
        labels = [d.strftime('%b') for d in dates]

    values = []
    for d in dates:
        if filter == 'daily':
            end = d + timedelta(days=1)
        elif filter == 'monthly':
            end = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        else:
            end = d.replace(year=d.year + 1)

        total = EmployeePayment.objects.filter(date__gte=d, date__lt=end).aggregate(s=Sum('amount'))['s'] or 0
        values.append(round(total, 2))

    return JsonResponse({'labels': labels, 'data': values})


@login_required
def export_employee_payment_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee', 'Date', 'Type', 'Amount', 'Method', 'Department'])

    for p in EmployeePayment.objects.select_related('employee', 'payment_method', 'type', 'department'):
        writer.writerow([
            p.employee.name,
            p.date,
            p.type.name,
            p.amount,
            p.payment_method.name,
            p.department.department_name,
        ])
    return response

# List View
@login_required
def payment_list(request):
    payments = EmployeePayment.objects.all()
    employees = Employee.objects.all()
    payment_types = EmployeePaymentType.objects.all()
    departments = Department.objects.all()
    return render(request, 'payment_list.html', {'payments': payments,'employees': employees,'payment_types': payment_types,'departments': departments,})
'''
# Add New Payment
@login_required
def add_payment(request):
    if request.method == 'POST':
        form = EmployeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment added successfully!')
            return redirect('payment_list')
    else:
        form = EmployeePaymentForm()
    return render(request, 'add_payment.html', {'form': form})
'''


from core.models import TaskStatus
from django.utils import timezone


@login_required
def add_payment(request):
    if request.method == 'POST':
        form = EmployeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.approved = False
            payment.approval_status = TaskStatus.objects.filter(name__iexact='Pending').first()
            payment.approved_by = None
            payment.approved_at = None
            payment.save()
            messages.success(request, 'Payment added successfully! Awaiting admin approval.')
            return redirect('payment_list')
    else:
        form = EmployeePaymentForm()
    return render(request, 'add_payment.html', {'form': form})


# Edit Payment
@login_required
def edit_payment(request, pk):
    payment = get_object_or_404(EmployeePayment, pk=pk)
    if request.method == 'POST':
        form = EmployeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully!')
            return redirect('payment_list')
    else:
        form = EmployeePaymentForm(instance=payment)
    return render(request, 'edit_payment.html', {'form': form, 'payment': payment})

# Delete Payment
@login_required
def delete_payment(request, pk):
    payment = get_object_or_404(EmployeePayment, pk=pk)
    payment.delete()
    messages.success(request, 'Payment deleted successfully!')
    return redirect('payment_list')






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest
from .forms import LeaveRequestForm, LeaveReviewForm
from django.contrib import messages

@login_required
def leave_list(request):
    if request.user.department == 'hr':
        leaves = LeaveRequest.objects.all().select_related('user')
    else:
        leaves = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'leave_list.html', {'leaves': leaves})

@login_required
def leave_apply(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, 'Leave request submitted.')
            return redirect('technician_dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_form.html', {'form': form})

@login_required
def leave_review(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        form = LeaveReviewForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request reviewed.')
            return redirect('leave-list')
    else:
        form = LeaveReviewForm(instance=leave)
    return render(request, 'leave_review.html', {'form': form, 'leave': leave})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def attendance_report_view(request):
    return render(request, 'attendance_report.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def leave_apply_view(request):
    return render(request, 'leave_apply.html')

@login_required
def leave_requests_view(request):
    return render(request, 'leave_requests.html')

@login_required
def leave_report_view(request):
    return render(request, 'leave_report.html')



from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def pending_payments_list(request):
    pending_status = TaskStatus.objects.filter(name__iexact='Pending').first()
    payments = EmployeePayment.objects.filter(approval_status=pending_status)
    return render(request, 'pending_payments_list.html', {'payments': payments})

@staff_member_required
def approve_payment(request, pk):
    payment = get_object_or_404(EmployeePayment, pk=pk)
    approved_status = TaskStatus.objects.filter(name__iexact='Accepted').first()
    payment.approval_status = approved_status
    payment.approved = True
    payment.approved_by = request.user
    payment.approved_at = timezone.now()
    payment.save()
    messages.success(request, 'Payment approved successfully.')
    return redirect('pending_payments_list')

@staff_member_required
def reject_payment(request, pk):
    payment = get_object_or_404(EmployeePayment, pk=pk)
    rejected_status = TaskStatus.objects.filter(name__iexact='Rejected').first()
    payment.approval_status = rejected_status
    payment.approved = False
    payment.approved_by = request.user
    payment.approved_at = timezone.now()
    payment.save()
    messages.success(request, 'Payment rejected.')
    return redirect('pending_payments_list')

