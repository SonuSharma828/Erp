from django.db.models import Count
from django.shortcuts import render
from employees.models import Employee
from projects.models import Project
from manage_tasks.models import Task
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#from projects.models import Project
import json
# Create your views here.
@login_required
def home(request):
    total_emp = Employee.objects.count()
    total_projects = Project.objects.count()
    pending_tasks = Task.objects.filter(status='pending').count()
    project_data = Project.objects.annotate(month=TruncMonth('startdate')).values('month').annotate(count=Count('name')).order_by('month')
    labels = []
    data = []
    for record in project_data:
        labels.append(record['month'].strftime('%B %Y'))
        data.append(record['count'])
    context = {
        'total_emp':total_emp,
        'total_project':total_projects,
        
        'pending_tasks': pending_tasks,
        'labels': json.dumps(labels),
        'data':json.dumps(data)
    }
    return render(request, 'home.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from dashboard.models import CustomUser

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            department = user.department.department_name.lower().strip() if user.department else None
            print(f"Logged in {user.is_superuser}, department: {department}")
            #print(f"department raw: '{user.department.department_name}'")
            #print(f"department raw: '{user.department.department_name.lower().strip()}'")
            #if user.is_superuser:
                #return redirect('home')
            if department == 'hr':
                return redirect('user_list')
            #elif department == 'technician':
                #return redirect('technician_dashboard')
            elif department == 'finance':
                #print("Finance redirect hit")
                return redirect('spp_dashboard')
            elif department == 'inventory':
                return redirect('stock_list')
            elif user.is_superuser:
                return redirect('home')
            else:
                return render(request,'default.html')  # or any default dashboard

        else:
            messages.error(request, "Invalid credentials or no account found.")
    return render(request, 'login.html')


# views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import AdminCreateUserForm

@user_passes_test(lambda u: u.is_superuser)  # only admin allowed
def create_user_view(request):
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('luser_list')  # or anywhere you want
    else:
        form = AdminCreateUserForm()
    return render(request, 'create_user.html', {'form': form})


# views.py
from django.shortcuts import get_object_or_404

@user_passes_test(lambda u: u.is_superuser)
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('luser_list')
    else:
        form = AdminCreateUserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


'''
# views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import CustomUser
from HRM.models import Department

@user_passes_test(lambda u: u.is_superuser)
def user_list_view(request):
    department_id = request.GET.get('department')
    print("GET department_id:", department_id)  # 🔍 Debug print
    departments = Department.objects.all()

    if department_id and department_id.strip() != "":
        users = CustomUser.objects.filter(department__sno=department_id)
        selected_department = int(department_id)
    else:
        users = CustomUser.objects.all()
        selected_department = None

    return render(request, 'user_list.html', {
        'users': users,
        'departments': departments,
        'selected_department': selected_department
    })
'''

from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import CustomUser
from HRM.models import Department

@user_passes_test(lambda u: u.is_superuser)
def user_list_view(request):
    department_id = request.GET.get('department')
    page_number = request.GET.get('page')
    
    departments = Department.objects.all()

    if department_id and department_id.strip() != "":
        users_queryset = CustomUser.objects.filter(department__sno=department_id)
        selected_department = int(department_id)
    else:
        users_queryset = CustomUser.objects.all()
        selected_department = None

    paginator = Paginator(users_queryset, 30)  # 30 users per page
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_list.html', {
        'users': page_obj,
        'page_obj': page_obj,
        'departments': departments,
        'selected_department': selected_department
    })




@user_passes_test(lambda u: u.is_superuser)
def delete_user_view(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
    return redirect('luser_list')








import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    dept = request.user.department_name
    template_name = f'dashboard/{dept}.html'

    # Full path to check if the template file exists
    template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)

    print("User Department:", dept)
    print("Checking Template Path:", template_path)

    if os.path.exists(template_path):
        return render(request, template_name)
    else:
        return render(request, 'dashboard/default.html')





# views.py

from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()
'''
@login_required
def invoice_list(request):
    company_id = request.GET.get('company')
    created_by = request.GET.get('created_by')

    invoices = Invoice.objects.select_related('company')

    if company_id:
        invoices = invoices.filter(company_id=company_id)

    if created_by:
        invoices = invoices.filter(created_by__id=created_by)

    companies = Company.objects.all()
    users = User.objects.filter(invoice__isnull=False).distinct()

    return render(request, 'invoice_list.html', {
        'invoices': invoices,
        'companies': companies,
        'users': users,
        'selected_company': company_id,
        'selected_user': created_by,
    })
'''

from django.core.paginator import Paginator

@login_required
def invoice_list(request):
    company_id = request.GET.get('company')
    created_by = request.GET.get('created_by')

    invoices = Invoice.objects.select_related('company')

    if company_id:
        invoices = invoices.filter(company_id=company_id)

    if created_by:
        invoices = invoices.filter(created_by__id=created_by)

    paginator = Paginator(invoices, 10)  # Show 10 invoices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    companies = Company.objects.all()
    users = User.objects.filter(invoice__isnull=False).distinct()

    return render(request, 'invoice_list.html', {
        'page_obj': page_obj,
        'companies': companies,
        'users': users,
        'selected_company': company_id,
        'selected_user': created_by,
    })
'''
@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form,'title': 'Create Invoice'})
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Invoice
from customer.models import Customer
from .forms import InvoiceForm

@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            # Assign the selected customer as client_name
            customer_id = request.POST.get('client_name')
            invoice.client_name = Customer.objects.get(id=customer_id)
            invoice.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()

    customers = Customer.objects.all()
    return render(request, 'create_invoice.html', {
        'form': form,
        'title': 'Create Invoice',
        'customers': customers
    })
'''
@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'edit_invoice.html', {'form': form,'title': 'Edit Invoice'})


@login_required
def edit_invoice(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            customer_id = request.POST.get('client_name')
            invoice.client_name = Customer.objects.get(id=customer_id)
            invoice.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)

    customers = Customer.objects.all()
    return render(request, 'edit_invoice.html', {
        'form': form,
        'title': 'Edit Invoice',
        'customers': customers
    })

'''

'''


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice
from customer.models import Customer
from .forms import InvoiceForm

@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            customer_id = request.POST.get('client_name')
            invoice.client_name = Customer.objects.get(id=customer_id)
            invoice.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()

    # ✅ Load only recent 50 customers for dropdown
    customers = Customer.objects.all()[:50]

    return render(request, 'create_invoice.html', {
        'form': form,
        'title': 'Create Invoice',
        'customers': customers,
        'selected_customer': None
    })

'''
@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            customer_id = request.POST.get('client_name')
            invoice.client_name = Customer.objects.get(id=customer_id)
            invoice.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)

    # ✅ Load recent 50 + selected customer (if not in recent 50)
    selected_customer = invoice.client_name
    customers = list(Customer.objects.all()[:50])
    if selected_customer not in customers:
        customers.append(selected_customer)

    return render(request, 'edit_invoice.html', {
        'form': form,
        'title': 'Edit Invoice',
        'customers': customers,
        'selected_customer': selected_customer
    })

@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('invoice_list')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Company, Invoice
from .forms import CompanyForm, InvoiceForm
'''
@user_passes_test(lambda u: u.is_superuser)
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})
'''

from django.core.paginator import Paginator

@user_passes_test(lambda u: u.is_superuser)
def company_list(request):
    companies = Company.objects.all().order_by('id')  # Optional: order consistently
    paginator = Paginator(companies, 10)  # Show 10 companies per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'company_list.html', {
        'page_obj': page_obj
    })

@user_passes_test(lambda u: u.is_superuser)
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'add_company.html', {'form': form,'title': 'Add Company'})



# views.py

@user_passes_test(lambda u: u.is_superuser)
def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'edit_company.html', {'form': form,'title': 'Edit Company'})


@user_passes_test(lambda u: u.is_superuser)
def delete_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return redirect('company_list')

