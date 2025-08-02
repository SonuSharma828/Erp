from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer,ContactPerson
from .forms import CustomerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 10)  # 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'customer_list.html', {'page_obj': page_obj})


'''
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
'''
'''
@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})
'''
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()

            # Handle Contact Persons
            total_contacts = int(request.POST.get('contacts-TOTAL_FORMS', 0))
            for i in range(total_contacts):
                name = request.POST.get(f'contacts-{i}-name')
                phone = request.POST.get(f'contacts-{i}-phone')
                if name and phone:
                    ContactPerson.objects.create(customer=customer, name=name, phone=phone)


            messages.success(request, 'Vendor added successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})

@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})

@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customer_list')
