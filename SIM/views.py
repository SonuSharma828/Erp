from django.shortcuts import render, get_object_or_404, redirect
from .models import DailyStatus, ExpenseApproval, PaymentFollowUp, Project, QuickJob
from .forms import DailyStatusForm, ExpenseApprovalForm, PaymentFollowUpForm, QuickJobForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from datetime import date
from django.utils.timezone import now
from django.shortcuts import render
from .models import *
from employees.models import Employee
from manage_tasks.models import Task, TaskBilling, ManualItem, ExternalExpense, CoWorkerCharge
from HRM.models import EmployeePayment
from spp.models import SalaryDeduction
from core.models import TaskStatus

def hp_summary(request):
    emp_id = request.GET.get('emp_id')
    employees = Employee.objects.all()

    if not emp_id and employees.exists():
        emp_id = employees.first().sno

    employee = get_object_or_404(Employee, pk=emp_id)

    # Dates
    start_date = request.GET.get('start_date', date.today().replace(day=1))
    end_date = request.GET.get('end_date', date.today())

    # Tasks
    tasks = Task.objects.filter(
        assigned_to=employee.user,
        date__range=[start_date, end_date]
    )
    total_tasks = tasks.count()



    completed_status = TaskStatus.objects.filter(name__iexact="Completed").first()
    rejected_status = TaskStatus.objects.filter(name__iexact="Rejected").first()
    pending_status = TaskStatus.objects.filter(name__iexact="Pending").first()
    print(completed_status)

    completed_tasks = Task.objects.filter(assigned_to__sno=employee.sno, status='completed',date__range=[start_date, end_date]).count()
    pending_tasks = Task.objects.filter(assigned_to__sno=employee.sno, status='pending',date__range=[start_date, end_date]).count()
    rejected_tasks = Task.objects.filter(assigned_to__sno=employee.sno, status='rejected',date__range=[start_date, end_date]).count()

    print(completed_tasks)
    print(pending_tasks)
    print(rejected_tasks)


    # Task earnings
    billings = TaskBilling.objects.filter(
        technician=employee, 
        submitted_at__date__range=[start_date, end_date]
    )
    tools_earning = billings.aggregate(total=Sum('tools_total'))['total'] or 0
    service_earning = billings.aggregate(total=Sum('service_total'))['total'] or 0
    final_total = billings.aggregate(total=Sum('final_total'))['total'] or 0

    # Expenses
    manual_total = ManualItem.objects.filter(task__in=tasks).aggregate(total=Sum('price'))['total'] or 0
    external_total = ExternalExpense.objects.filter(task__in=tasks).aggregate(total=Sum('price'))['total'] or 0
    coworker_total = CoWorkerCharge.objects.filter(task__in=tasks).aggregate(total=Sum('charge'))['total'] or 0
    total_expenses = manual_total + external_total + coworker_total

    # Salary + Payment
    salary = employee.salary
    payments = EmployeePayment.objects.filter(employee=employee, date__range=[start_date, end_date])
    total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0

    # Deductions
    deductions = SalaryDeduction.objects.filter(employee=employee, date__range=[start_date, end_date])
    total_deductions = deductions.aggregate(total=Sum('amount'))['total'] or 0

    # Profitability
    net_profit = final_total - total_expenses - total_deductions

    context = {
        'employee': employee,
        'employees': employees,
        'task_stats': {
            'total': total_tasks,
            'completed': completed_tasks,
            'rejected': rejected_tasks,
            'pending':pending_tasks,
        },
        'earnings': {
            'tools': tools_earning,
            'service': service_earning,
            'final': final_total,
        },
        'expenses': {
            'manual': manual_total,
            'external': external_total,
            'coworker': coworker_total,
            'total': total_expenses,
        },
        'salary': salary,
        'total_paid': total_paid,
        'deductions': total_deductions,
        'net_profit': net_profit,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'hp_summary.html', context)




@login_required
def daily_status_list(request):
    statuses = DailyStatus.objects.all()
    return render(request, 'daily_status_list.html', {'statuses': statuses})

@login_required
def add_daily_status(request):
    if request.method == 'POST':
        form = DailyStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_status_list')
    else:
        form = DailyStatusForm()
    return render(request, 'add_daily_status.html', {'form': form})

@login_required
def edit_daily_status(request, pk):
    status = get_object_or_404(DailyStatus, pk=pk)
    if request.method == 'POST':
        form = DailyStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('daily_status_list')
    else:
        form = DailyStatusForm(instance=status)
    return render(request, 'edit_daily_status.html', {'form': form})

@login_required
def delete_daily_status(request, pk):
    status = get_object_or_404(DailyStatus, pk=pk)
    status.delete()
    return redirect('daily_status_list')


@login_required
def payment_followup_list(request):
    followups = PaymentFollowUp.objects.all()
    return render(request, 'payment_followup_list.html', {'followups': followups})

@login_required
def add_payment_followup(request):
    if request.method == 'POST':
        form = PaymentFollowUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_followup_list')
    else:
        form = PaymentFollowUpForm()
    return render(request, 'add_payment_followup.html', {'form': form})

@login_required
def edit_payment_followup(request, pk):
    followup = get_object_or_404(PaymentFollowUp, pk=pk)
    if request.method == 'POST':
        form = PaymentFollowUpForm(request.POST, instance=followup)
        if form.is_valid():
            form.save()
            return redirect('payment_followup_list')
    else:
        form = PaymentFollowUpForm(instance=followup)
    return render(request, 'edit_payment_followup.html', {'form': form})

@login_required
def delete_payment_followup(request, pk):
    followup = get_object_or_404(PaymentFollowUp, pk=pk)
    followup.delete()
    return redirect('payment_followup_list')

@login_required
def quickjob_list(request):
    jobs = QuickJob.objects.all()
    return render(request, 'quickjob_list.html', {'jobs': jobs})

@login_required
def add_quickjob(request):
    if request.method == 'POST':
        form = QuickJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quickjob_list')
    else:
        form = QuickJobForm()
    return render(request, 'add_quickjob.html', {'form': form})

@login_required
def edit_quickjob(request, pk):
    job = get_object_or_404(QuickJob, pk=pk)
    if request.method == 'POST':
        form = QuickJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('quickjob_list')
    else:
        form = QuickJobForm(instance=job)
    return render(request, 'edit_quickjob.html', {'form': form})

@login_required
def delete_quickjob(request, pk):
    job = get_object_or_404(QuickJob, pk=pk)
    job.delete()
    return redirect('quickjob_list')

'''
@login_required
def expense_list(request):
    expenses = ExpenseApproval.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})
'''
from django.core.paginator import Paginator

@login_required
def expense_list(request):
    expenses = ExpenseApproval.objects.all().order_by('-entry_date')
    paginator = Paginator(expenses, 10)  # Show 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'expense_list.html', {'page_obj': page_obj})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseApprovalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseApprovalForm()
    return render(request, 'add_expensesss.html', {'form': form})

@login_required
def bulk_approve_expenses(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_expenses')
        ExpenseApproval.objects.filter(id__in=ids).update(status='Approved')
    return redirect('expense_list')



from django.shortcuts import render, redirect, get_object_or_404
from .models import SIMJob
from .forms import SIMJobForm

@login_required
def simjob_list(request):
    jobs = SIMJob.objects.all().order_by('-start_date')
    return render(request, 'simjob_list.html', {'jobs': jobs})

@login_required
def simjob_add(request):
    if request.method == 'POST':
        form = SIMJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('simjob_list')
    else:
        form = SIMJobForm()
    return render(request, 'simjob_form.html', {'form': form, 'title': 'Add Job'})

@login_required
def simjob_edit(request, pk):
    job = get_object_or_404(SIMJob, pk=pk)
    if request.method == 'POST':
        form = SIMJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('simjob_list')
    else:
        form = SIMJobForm(instance=job)
    return render(request, 'simjob_form.html', {'form': form, 'title': 'Edit Job'})

@login_required
def simjob_delete(request, pk):
    job = get_object_or_404(SIMJob, pk=pk)
    job.delete()
    return redirect('simjob_list')
    

