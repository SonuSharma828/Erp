from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task,ServiceCharge
from django.contrib.auth.decorators import login_required
from core.models import TaskImportance,TaskStatus
from django.contrib.auth import get_user_model
from employees.models import Employee
from django.core.paginator import Paginator
from customer.models import Customer


from django.http import JsonResponse

@login_required
def task_list(request):
    tasks_qs = Task.objects.all().order_by('-created_at')
    priorities = TaskImportance.objects.all()
    statuses = TaskStatus.objects.all()
    users = get_user_model().objects.filter(is_active=True)

    # Pagination
    paginator = Paginator(tasks_qs, 10)  # Show 25 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_list.html', {
        'tasks': page_obj,
        'page_obj': page_obj,
        'priorities': priorities,
        'statuses': statuses,
        'users': users,
    })

from django.db.models import Max

@login_required
def add_task(request):
    if request.method == 'POST':
        # Find next available sno
        last_sno = Task.objects.aggregate(Max('sno'))['sno__max'] or 0
        next_sno = last_sno + 1

        task = Task()
        task.sno = next_sno  # Manually set sno
        task.task_detail = request.POST.get('task_detail')
        task.date = request.POST.get('date')
        task.priority = request.POST.get('priority')
        task.location = request.POST.get('location')
        task.customer_id = request.POST.get('customer')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.service_id = request.POST.get('service')
        task.created_by = request.user
        task.save()
        return redirect('task_list')

    # Dropdown data
    priorities = TaskImportance.objects.all()
    employees = Employee.objects.all()
    customers = Customer.objects.all()
    services = ServiceCharge.objects.all()

    return render(request, 'add_task.html', {
        'priorities': priorities,
        'employees': employees,
        'customers': customers,
        'services': services,
    })
'''
@login_required
def edit_task(request, sno):
    task = get_object_or_404(Task, sno=sno)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})
'''

from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def edit_task(request, sno):
    task = get_object_or_404(Task, sno=sno)

    if request.method == 'POST':
        task.task_detail = request.POST.get('task_detail')
        task.date = request.POST.get('date')
        task.priority = request.POST.get('priority')
        task.location = request.POST.get('location')
        task.customer_id = request.POST.get('customer')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.service_id = request.POST.get('service')
        task.save()
        return redirect('task_list')

    # Dropdown data
    priorities = TaskImportance.objects.all()
    employees = Employee.objects.all()
    customers = Customer.objects.all()
    services = ServiceCharge.objects.all()

    return render(request, 'edit_task.html', {
        'task': task,
        'priorities': priorities,
        'employees': employees,
        'customers': customers,
        'services': services,
    })

@login_required
def delete_task(request, sno):
    task = get_object_or_404(Task, sno=sno)
    task.delete()
    return redirect('task_list')



from django.db.models import Sum, Count
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
from django.utils.timezone import now
from manage_tasks.models import TaskBilling  # adjust import if needed

@login_required
def task_earning_dashboard(request):
    # Breakdown by Technician
    technician_breakdown = TaskBilling.objects.values('technician__name').annotate(total=Sum('final_total'))

    # Breakdown by Payment Mode
    mode_breakdown = TaskBilling.objects.values('payment_mode__name').annotate(total=Sum('final_total'))

    context = {
        'technician_breakdown': technician_breakdown,
        'mode_breakdown': mode_breakdown
    }
    return render(request, 'task_earning_dashboard.html', context)


@login_required
def task_earning_chart_data(request):
    filter = request.GET.get('filter', 'monthly')
    today = now().date()

    if filter == 'daily':
        date_list = [today - timedelta(days=i) for i in reversed(range(7))]
        label_list = [d.strftime('%d %b') for d in date_list]
    elif filter == 'yearly':
        date_list = [datetime(today.year - i, 1, 1).date() for i in reversed(range(3))]
        label_list = [d.strftime('%Y') for d in date_list]
    else:  # monthly
        date_list = [datetime(today.year, i, 1).date() for i in range(1, 13)]
        label_list = [d.strftime('%b') for d in date_list]

    values = []
    for d in date_list:
        if filter == 'daily':
            end = d + timedelta(days=1)
        elif filter == 'monthly':
            end = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        else:
            end = d.replace(year=d.year + 1)

        total = TaskBilling.objects.filter(submitted_at__date__gte=d, submitted_at__date__lt=end).aggregate(s=Sum('final_total'))['s'] or 0
        values.append(round(total, 2))

    return JsonResponse({'labels': label_list, 'data': values})


@login_required
def export_task_earning_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task_earnings.csv"'

    writer = csv.writer(response)
    writer.writerow(['Task ID', 'Technician', 'Service Total', 'Tools Total', 'Final Total', 'Payment Mode', 'Submitted At'])

    for entry in TaskBilling.objects.select_related('task', 'technician', 'payment_mode'):
        writer.writerow([
            entry.task.sno,
            entry.technician.name,
            entry.service_total,
            entry.tools_total,
            entry.final_total,
            entry.payment_mode.name,
            entry.submitted_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response


from django.shortcuts import render, redirect, get_object_or_404
from .models import ServiceCharge
from .forms import ServiceChargeForm

'''
@login_required
def service_charge_list(request):
    services = ServiceCharge.objects.all()
    form = ServiceChargeForm()
    
    if request.method == 'POST':
        form = ServiceChargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service-charges-list')

    return render(request, 'service_charge_list.html', {
        'services': services,
        'form': form,
    })
'''


from django.core.paginator import Paginator

@login_required
def service_charge_list(request):
    form = ServiceChargeForm()

    if request.method == 'POST':
        form = ServiceChargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service-charges-list')

    service_list = ServiceCharge.objects.all().order_by('-id')
    paginator = Paginator(service_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'service_charge_list.html', {
        'form': form,
        'page_obj': page_obj,
        'total_services': paginator.count
    })

@login_required
def service_charge_edit(request, pk):
    service = get_object_or_404(ServiceCharge, pk=pk)
    form = ServiceChargeForm(instance=service)

    if request.method == 'POST':
        form = ServiceChargeForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service-charges-list')

    return render(request, 'service_charge_edit.html', {
        'form': form,
        'service': service,
    })

@login_required
def service_charge_delete(request, pk):
    service = get_object_or_404(ServiceCharge, pk=pk)
    service.delete()
    return redirect('service-charges-list')
