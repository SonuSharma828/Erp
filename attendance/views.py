from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance
from .forms import AttendanceForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from django.db.models import Q
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
@login_required
def attendance_list(request):
    user_id = request.GET.get('user')
    date = request.GET.get('date')

    records = Attendance.objects.select_related('user').order_by('-date')

    if user_id:
        records = records.filter(user_id=user_id)
    if date:
        records = records.filter(date=date)
    
    users = User.objects.all()
    return render(request, 'attendance_list.html', {
        'records': records,
        'users': users,
        'selected_user': user_id,
        'selected_date': date,
    })

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list1')
    else:
        form = AttendanceForm(initial={'date': now().date()})
    return render(request, 'attendance_form.html', {'form': form})

@login_required
def edit_attendance(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('attendance_list1')
    else:
        form = AttendanceForm(instance=record)
    return render(request, 'attendance_form.html', {'form': form})


from calendar import monthrange

@login_required
def monthly_report(request, user_id):
    from datetime import date
    user = get_object_or_404(User, pk=user_id)
    month = int(request.GET.get('month', now().month))
    year = int(request.GET.get('year', now().year))

    days_in_month = monthrange(year, month)[1]
    records = Attendance.objects.filter(user=user, date__year=year, date__month=month)

    # Count each status
    summary = {
        'present': records.filter(status='present').count(),
        'absent': records.filter(status='absent').count(),
        'leave': records.filter(status='leave').count(),
        'half': records.filter(status='half').count(),
    }

    return render(request, 'monthly_report.html', {
        'user': user,
        'records': records,
        'month': month,
        'year': year,
        'days_in_month': days_in_month,
        'summary': summary
    })

