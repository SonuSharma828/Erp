from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskGroup
from django.contrib.auth.decorators import login_required
from django.utils import timezone
'''
@login_required
def task_group_list(request):
    groups = TaskGroup.objects.all()
    return render(request, 'task_group.html', {'groups': groups})
'''

from django.core.paginator import Paginator

@login_required
def task_group_list(request):
    groups_list = TaskGroup.objects.all().order_by('-created_at')
    paginator = Paginator(groups_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_group.html', {
        'page_obj': page_obj,
    })

@login_required
def add_task_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        TaskGroup.objects.create(
            task_group_name=name,
            created_by=request.user,
            created_at=timezone.now()
        )
        return redirect('task_group_list')
    return render(request, 'add_task_group.html')

@login_required
def delete_task_group(request, sno):
    group = get_object_or_404(TaskGroup, sno=sno)
    group.delete()
    return redirect('task_group_list')

@login_required
def edit_task_group(request, sno):
    group = get_object_or_404(TaskGroup, sno=sno)
    if request.method == 'POST':
        group.task_group_name = request.POST.get('name')
        group.save()
        return redirect('task_group_list')
    return render(request, 'edit_task_group.html', {'group': group})
