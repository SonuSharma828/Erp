from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Supplier, ContactPerson, Bill
from .forms import SupplierForm, ContactPersonForm, BillForm
from django.contrib import messages
'''
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.prefetch_related('contacts', 'bills').all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})
'''
from django.core.paginator import Paginator

@login_required
def supplier_list(request):
    supplier_list = Supplier.objects.prefetch_related('contacts', 'bills').all()
    paginator = Paginator(supplier_list, 10)  # Show 10 suppliers per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'supplier_list.html', {'page_obj': page_obj})


def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()

            # Handle Contact Persons
            total_contacts = int(request.POST.get('contacts-TOTAL_FORMS', 0))
            for i in range(total_contacts):
                name = request.POST.get(f'contacts-{i}-name')
                phone = request.POST.get(f'contacts-{i}-phone')
                if name and phone:
                    ContactPerson.objects.create(supplier=supplier, name=name, phone=phone)

            # Handle Bills
            total_bills = int(request.POST.get('bills-TOTAL_FORMS', 0))
            for i in range(total_bills):
                bill_number = request.POST.get(f'bills-{i}-bill_number')
                bill_date = request.POST.get(f'bills-{i}-bill_date')
                amount = request.POST.get(f'bills-{i}-amount')
                description = request.POST.get(f'bills-{i}-description')
                invoice = request.FILES.get(f'bills-{i}-invoice')
                if bill_number and amount and bill_date:
                    Bill.objects.create(
                        supplier=supplier,
                        bill_number=bill_number,
                        bill_date=bill_date,
                        amount=amount,
                        description=description,
                        invoice=invoice
                    )

            messages.success(request, 'Vendor added successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'add_supplier.html', {'form': form})

@login_required
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})

@login_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')





def show_bill_details(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    bills = supplier.bills.all()
    print("BILLS FOUND:", bills)
    return render(request, 'bill_details.html', {'supplier': supplier, 'bills': bills})
