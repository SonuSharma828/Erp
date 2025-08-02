from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ProjectForm , TaskForm, CommentForm
import json
from django.contrib.auth.decorators import login_required
from core.models import ProjectStatus
from customer.models import Customer

from django.http import JsonResponse
from django.core.paginator import Paginator
from customer.models import Customer

def paginated_customers(request):
    search_query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    page_size = 20

    customers = Customer.objects.all()
    if search_query:
        customers = customers.filter(customer_name__icontains=search_query)

    paginator = Paginator(customers, page_size)
    page = paginator.get_page(page_number)

    data = {
        "results": [{"id": c.id, "name": c.customer_name} for c in page.object_list],
        "has_next": page.has_next(),
        "has_prev": page.has_previous(),
        "page": page.number,
        "total_pages": paginator.num_pages,
    }
    return JsonResponse(data)


# Create your views here.
'''
@login_required
def project(request):
    projects = Project.objects.all()
    statuses = ProjectStatus.objects.all()
    clients = Customer.objects.all()
    return render(request, 'project.html', {'projects': projects,'statuses': statuses,'clients': clients,})
'''

from django.core.paginator import Paginator
'''
@login_required
def project(request):
    project_list = Project.objects.all()
    paginator = Paginator(project_list, 10)  # 10 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    statuses = ProjectStatus.objects.all()
    client_ids = page_obj.object_list.values_list('client_id', flat=True).distinct()
    clients1 = Customer.objects.filter(id__in=client_ids)
    
    return render(request, 'project.html', {
        'page_obj': page_obj,
        'statuses': statuses,
        'clients1': clients1,
    })
'''

@login_required
def project(request):
    # Fetch all projects, with their clients
    project_list = Project.objects.select_related('client').all()

    # Extract unique client IDs *before* slicing
    client_ids = project_list.values_list('client_id', flat=True).distinct()
    clients1 = Customer.objects.filter(id__in=client_ids)

    # Now paginate
    paginator = Paginator(project_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    statuses = ProjectStatus.objects.all()

    return render(request, 'project.html', {
        'page_obj': page_obj,
        'statuses': statuses,
        'clients1': clients1,
    })

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project:project')
        else:
            print("form is invalid")
            print(f"form error : {form.errors}")
        
    else:
        form = ProjectForm()
        customers = Customer.objects.all()
    return render(request, 'add_project.html', {'form': form,'customers': customers})


#edit employee details 
'''
@login_required  
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('project:project')
        else:
            print("form is invalid")
            print(f"form error : {form.errors}")
    else:
        form = ProjectForm(instance=project)
        customers = Customer.objects.all()
    return render(request, 'edit_project.html', {'form': form, 'project': project,'customers': customers})
'''

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    customers = Customer.objects.all()  # ✅ Always load this

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project:project')
        else:
            print("form is invalid")
            print(f"form error : {form.errors}")
    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {
        'form': form,
        'project': project,
        'customers': customers
    })


   
#delete employee data

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project:project')

