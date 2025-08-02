from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required

'''
# Create employee lading page here.
@login_required
def employees(request):
    employees = Employee.objects.all()
    return render(request, 'employee.html', {'employees': employees})
'''

from django.core.paginator import Paginator

@login_required
def employees(request):
    employee_list = Employee.objects.all().order_by('-sno')
    paginator = Paginator(employee_list, 10)  # Show 20 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employee.html', {
        'employees': page_obj,
        'page_obj': page_obj,
    })


from django.shortcuts import render, get_object_or_404
from .models import Employee
from spp.models import MonthlyExpense, SalaryDeduction  
from manage_tasks.models import Task,TaskBilling  
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    # Related records
    expenses = MonthlyExpense.objects.filter(employee=employee)
    deductions = SalaryDeduction.objects.filter(employee=employee)
    tasks_completed = Task.objects.filter(assigned_to=employee.user, status='completed')
    tasks_pending = Task.objects.filter(assigned_to=employee.user).exclude(status='completed')
    tasks = Task.objects.filter(assigned_to__email=employee.email)
    bills = TaskBilling.objects.filter(technician__email=employee.email).order_by('-submitted_at')
    total_deductions = deductions.aggregate(total=models.Sum('amount'))['total'] or 0
    total_expenses = expenses.aggregate(total=models.Sum('amount'))['total'] or 0
    final_salary = employee.salary - total_deductions

    context = {
        'employee': employee,
        'expenses': expenses,
        'deductions': deductions,
        'tasks_completed': tasks_completed,
        'tasks_pending': tasks_pending,
        'total_deductions': total_deductions,
        'total_expenses': total_expenses,
        'final_salary': final_salary,
        'tasks': tasks,
        'bills': bills,
    }

    return render(request, 'employee_detail.html', context)

# add employee logic
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee:employee')
        else:
            print("form is invalid")
            print(f"form error : {form.errors}")
    else:
        form = EmployeeForm()
          
    return render(request, 'add_employee.html', {'form':form})


 #edit employee details 
@login_required  
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES ,instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee:employee')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})



#delete employee data
@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee:employee')

