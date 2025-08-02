from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from manage_tasks.models import Task
from attendance.models import Attendance
from STK.models import STKTake
from datetime import date
from django.db.models import Count
from django.utils.timezone import now

@login_required
def technician_dashboard(request):
    user = request.user
    today = date.today()

    # Task stats
    task_counts = Task.objects.filter(assigned_to=user).values('status').annotate(count=Count('id'))

    # Attendance today
    try:
        attendance_today = Attendance.objects.get(user=user, date=today)
    except Attendance.DoesNotExist:
        attendance_today = None

    # Equipment issued today
    issued_today = STKTake.objects.filter(issued_to=user, issue_date__date=today)

    context = {
        'task_counts': task_counts,
        'attendance_today': attendance_today,
        'issued_today': issued_today,
    }
    return render(request, 'temdash.html', context)

from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def technician_task_list(request):
    user = request.user
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    tasks = Task.objects.filter(assigned_to=user)

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    paginator = Paginator(tasks.order_by('-scheduled_date'), 10)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'query': query,
    }
    return render(request, 'task_list.html', context)


from django.shortcuts import get_object_or_404, redirect

@login_required
def technician_task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES).keys():
            task.status = new_status
            task.save()
            return redirect('technician_task_list')

    context = {'task': task}
    return render(request, 'task_detail.html', context)



from django.db.models import Count
from django.http import JsonResponse

@login_required
def technician_dashboard(request):
    user = request.user
    task_status_data = (
        Task.objects.filter(assigned_to=user)
        .values('status')
        .annotate(count=Count('id'))
    )
    context = {
        'status_counts': {item['status']: item['count'] for item in task_status_data}
    }
    return render(request, 'temdash.html', context)



@login_required
def equipment_log(request):
    user = request.user
    records = IssueRecord.objects.filter(issued_to=user).order_by('-issue_date')

    context = {
        'records': records
    }
    return render(request, 'equipment_log.html', context)



@login_required
def task_report(request):
    user = request.user
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    tasks = Task.objects.filter(assigned_to=user)

    if from_date and to_date:
        tasks = tasks.filter(scheduled_date__range=[from_date, to_date])

    return render(request, 'task_report.html', {
        'tasks': tasks,
        'from_date': from_date,
        'to_date': to_date,
    })



# technician/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from HRM.forms import LeaveRequestForm

@login_required
def technician_leave_apply(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = 'pending'  # if you have a status field
            leave.save()
            messages.success(request, 'Leave request submitted.')
            return redirect('technician_dashboard')  # change as needed
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_apply.html', {'form': form})



# technician/views.py
from HRM.models import LeaveRequest  # still using HR's Leave model

@login_required
def technician_leave_list(request):
    leaves = LeaveRequest.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'leave_list.html', {'leaves': leaves})

