import csv
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render,redirect, get_object_or_404
from .models import (
    SparePartTransaction,
    MonthlySale,
    MonthlyExpense,
    MonthlyVendorPayment,
    VendorPaymentEntry,
)
from django.db.models import Sum
from django.shortcuts import render
from .models import SparePart
from .forms import SparePartTransactionForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from core.models import PaymentMode,ExpenseType,AmountType
from dashboard.models import Company
from STK.models import STKStock
from employees.models import Employee
from HRM.models import EmployeePayment
from manage_tasks.models import TaskBilling


@login_required
def spp_dashboard(request):
    # profit
    total_sales = MonthlySale.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_task_amount = TaskBilling.objects.aggregate(Sum('final_total'))['final_total__sum'] or 0
    #loss  
    total_expenses = MonthlyExpense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_vendor_payments = VendorPaymentEntry.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_employee_payments = EmployeePayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Totals
    total_income = total_sales + total_task_amount
    total_spending = total_expenses + total_vendor_payments + total_employee_payments

    net_pal = total_income - total_spending
    # Transaction Count (for fun metrics)
    #total_transactions = SparePartTransaction.objects.count()

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_vendor_payments': total_vendor_payments,
        #'total_gross_payments': total_gross_payments,
        'total_employee_payments':total_employee_payments,
        'total_task_amount':total_task_amount,
        'total_income': total_income,
        'total_spending': total_spending,
        'net_pal': net_pal,
        #'total_transactions': total_transactions,
    }

    return render(request, 'spp_dashboard.html', context)

'''
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date, timedelta
from .models import MonthlySale, MonthlyExpense, MonthlyVendorPayment

def get_finance_summary(request):
    filter_type = request.GET.get('filter', 'monthly')

    today = date.today()

    if filter_type == 'daily':
        start_date = today
    elif filter_type == 'monthly':
        start_date = today.replace(day=1)
    elif filter_type == 'yearly':
        start_date = today.replace(month=1, day=1)
    else:
        return JsonResponse({'error': 'Invalid filter'}, status=400)

    sales = MonthlySale.objects.filter(date__gte=start_date).aggregate(total=Sum('total_sales'))['total'] or 0
    task = TaskBilling.objects.filter(submitted_at__date__gte=start_date).aggregate(total=Sum('amount'))['total'] or 0
    expenses = MonthlyExpense.objects.filter(date__gte=start_date).aggregate(total=Sum('amount'))['total'] or 0
    vendor = MonthlyVendorPayment.objects.filter(date__gte=start_date).aggregate(total=Sum('total_amount'))['total'] or 0
    employee = EmployeePayment.objects.filter(date__gte=start_date).aggregate(total=Sum('amount'))['total'] or 0

    return JsonResponse({
        'sales': round(sales, 2),
        'task': round(task, 2),
        'expenses': round(expenses, 2),
        'vendor': round(vendor, 2),
        'employee': round(employee, 2)
    })

'''

from django.http import JsonResponse
from datetime import date
from django.db.models import Sum
from .models import MonthlySale
from manage_tasks.models import TaskBilling
from .models import MonthlyExpense
from .models import MonthlyVendorPayment
from HRM.models import EmployeePayment

def get_finance_summary(request):
    try:
        filter_type = request.GET.get('filter', 'monthly')
        today = date.today()

        if filter_type == 'daily':
            start_date = today
        elif filter_type == 'monthly':
            start_date = today.replace(day=1)
        elif filter_type == 'yearly':
            start_date = today.replace(month=1, day=1)
        else:
            return JsonResponse({'error': 'Invalid filter'}, status=400)

        sales = MonthlySale.objects.filter(date__gte=start_date).aggregate(total=Sum('total_sales'))['total'] or 0
        task = TaskBilling.objects.filter(submitted_at__date__gte=start_date).aggregate(total=Sum('final_total'))['total'] or 0
        expenses = MonthlyExpense.objects.filter(date__gte=start_date).aggregate(total=Sum('amount'))['total'] or 0
        vendor = MonthlyVendorPayment.objects.filter(date__gte=start_date).aggregate(total=Sum('amount'))['total'] or 0

        employee = EmployeePayment.objects.filter(date__gte=start_date).aggregate(total=Sum('amount'))['total'] or 0

        return JsonResponse({
            'sales': round(sales, 2),
            'task': round(task, 2),
            'expenses': round(expenses, 2),
            'vendor': round(vendor, 2),
            'employee': round(employee, 2)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def manage_spareparts(request):
    spareparts = SparePart.objects.all()
    return render(request, 'manage_spareparts.html', {'spareparts': spareparts})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = SparePartTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SparePartTransactionForm()
    return render(request, 'add_transaction_form.html', {'form': form})
'''
@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="spp_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Total Sales', 'Total Expenses', 'Total Vendor Payments', 'Gross Profit/Loss'])

    total_sales = MonthlySale.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = MonthlyExpense.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_vendor_payments = MonthlyVendorPayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    gross_profit = total_sales - (total_expenses + total_vendor_payments)

    writer.writerow([total_sales, total_expenses, total_vendor_payments, gross_profit])

    return response
'''



@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="finance_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Total Sales',
        'Total Task Earnings',
        'Total Expenses',
        'Total Vendor Payments',
        'Total Employee Payments',
        'Net Profit / Loss'
    ])

    # Income
    total_sales = MonthlySale.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_task_amount = TaskBilling.objects.aggregate(total=Sum('final_total'))['total'] or 0

    # Expenses
    total_expenses = MonthlyExpense.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_vendor_payments = VendorPaymentEntry.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_employee_payments = EmployeePayment.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Net PAL calculation
    total_income = total_sales + total_task_amount
    total_spending = total_expenses + total_vendor_payments + total_employee_payments
    net_pal = total_income - total_spending

    writer.writerow([
        f"{total_sales:.2f}",
        f"{total_task_amount:.2f}",
        f"{total_expenses:.2f}",
        f"{total_vendor_payments:.2f}",
        f"{total_employee_payments:.2f}",
        f"{net_pal:.2f}"
    ])

    return response



from django.shortcuts import render, redirect
from .models import Voucher
from .forms import VoucherForm
from django.http import JsonResponse

# View to create a new voucher
@login_required
def create_voucher(request):
    if request.method == 'POST':
        form = VoucherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voucher_history')
    else:
        form = VoucherForm()
    return render(request, 'create_voucher.html', {'form': form})

@login_required
def edit_voucher(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    if request.method == 'POST':
        form = VoucherForm(request.POST, instance=voucher)
        if form.is_valid():
            form.save()
            return redirect('voucher_history')
    else:
        form = VoucherForm(instance=voucher)
    return render(request, 'edit_voucher.html', {'form': form})

@login_required
def delete_voucher(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    voucher.delete()
    return redirect('voucher_history')

# View to list all vouchers in the history
@login_required
def voucher_history(request):
    vouchers = Voucher.objects.all()
    return render(request, 'voucher_history.html', {'vouchers': vouchers})



from django.shortcuts import render, redirect
from .models import MonthlySale, MonthlyExpense, MonthlyVendorPayment
from .forms import MonthlySaleForm, MonthlyExpenseForm, MonthlyVendorPaymentForm
'''
@login_required
def manage_sales(request):
    #sales = MonthlySale.objects.all()
    sales = MonthlySale.objects.prefetch_related('payments', 'product').all()
    companies = Company.objects.all()
    products = STKStock.objects.all()
    return render(request, 'manage_sales.html', {'sales': sales,'companies': companies,'products': products,})
'''

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def manage_sales(request):
    sales_list = MonthlySale.objects.prefetch_related('payments', 'product').all().order_by('-date')
    
    paginator = Paginator(sales_list, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    companies = Company.objects.all()
    products = STKStock.objects.all()

    return render(request, 'manage_sales.html', {
        'sales': page_obj,
        'companies': companies,
        'products': products,
        'page_obj': page_obj,
    })



from django.shortcuts import render, redirect
from .forms import MonthlySaleForm, PaymentEntryFormSet
from .models import MonthlySale, PaymentEntry

def add_sales(request):
    if request.method == 'POST':
        sale_form = MonthlySaleForm(request.POST)
        
        # Get number of dynamic payment forms
        total = int(request.POST.get('payments-TOTAL_FORMS', 0))

        # Prepare list of payments from POST data
        payments = []
        for i in range(total):
            payment_type = request.POST.get(f'payments-{i}-payment_type')
            amount = request.POST.get(f'payments-{i}-amount')
            if payment_type and amount:
                payments.append({
                    'payment_type': payment_type,
                    'amount': float(amount)
                })

        if sale_form.is_valid():
            sale = sale_form.save()  # auto-sets date via model default

            for entry in payments:
                PaymentEntry.objects.create(
                    sale=sale,
                    payment_type=entry['payment_type'],
                    amount=entry['amount']
                )

            return redirect('manage_sales')  # ✅ replace with your actual list view name

    else:
        sale_form = MonthlySaleForm()

    return render(request, 'add_sales.html', {
        'sale_form': sale_form,
    })


from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import MonthlySale

from django.db.models import Sum, Count
import csv
from django.http import HttpResponse

@login_required
def sales_dashboard(request):
    # You can add filter controls here if needed later
    products = MonthlySale.objects.values('product__item_name').annotate(total=Sum('amount'))
    companies = MonthlySale.objects.values('company__name').annotate(total=Sum('amount'))
    payment_status = {
        "Settled": 0,
        "Pending": 0,
        "Overpaid": 0
    }

    for sale in MonthlySale.objects.all():
        msg = sale.payment_message()
        if "Pending" in msg:
            payment_status["Pending"] += 1
        elif "Overpaid" in msg:
            payment_status["Overpaid"] += 1
        else:
            payment_status["Settled"] += 1

    context = {
        "products": products,
        "companies": companies,
        "payment_status": payment_status,
    }
    return render(request, 'sales_dashboard.html', context)

@login_required
def sales_chart_data(request):
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

        total = MonthlySale.objects.filter(date__gte=d, date__lt=end).aggregate(s=Sum('amount'))['s'] or 0
        values.append(round(total, 2))

    return JsonResponse({'labels': label_list, 'data': values})


# Expenses 
@login_required
def add_expenses(request):
    if request.method == 'POST':
        form = MonthlyExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_expenses')
    else:
        form = MonthlyExpenseForm()
    return render(request, 'add_expenses.html', {'form': form})
'''
@login_required
def manage_expenses(request):
    expenses = MonthlyExpense.objects.all()
    companies = Company.objects.all()
    expense_types = ExpenseType.objects.all()
    amount_type = AmountType.objects.all()
    employees = Employee.objects.all()
    return render(request, 'manage_expenses.html', {'expenses': expenses,'companies': companies,'expense_types': expense_types,'amount_type':amount_type, 'employees': employees,})
'''

from django.core.paginator import Paginator

@login_required
def manage_expenses(request):
    expenses = MonthlyExpense.objects.all().order_by('-date')  # Optional: newest first
    paginator = Paginator(expenses, 10)  # Show 10 expenses per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'companies': Company.objects.all(),
        'expense_types': ExpenseType.objects.all(),
        'amount_type': AmountType.objects.all(),
        'employees': Employee.objects.all(),
    }
    return render(request, 'manage_expenses.html', context)




from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.http import JsonResponse, HttpResponse
import csv

from .models import MonthlyExpense  # Update this if model is in a different app

@login_required
def total_expense_dashboard(request):
    # Breakdown by company and type
    by_company = MonthlyExpense.objects.values('company__name').annotate(total=Sum('amount'))
    by_type = MonthlyExpense.objects.values('expense_type').annotate(total=Sum('amount'))
    by_atype = MonthlyExpense.objects.values('amount_type').annotate(total=Sum('amount'))
    context = {
        'by_company': by_company,
        'by_type': by_type,
        'by_atype':by_atype,
    }
    return render(request, 'total_expense_dashboard.html', context)


@login_required
def total_expense_chart_data(request):
    filter = request.GET.get('filter', 'monthly')
    today = now().date()

    if filter == 'daily':
        dates = [today - timedelta(days=i) for i in reversed(range(7))]
        labels = [d.strftime('%d %b') for d in dates]
    elif filter == 'yearly':
        dates = [datetime(today.year - i, 1, 1).date() for i in reversed(range(3))]
        labels = [d.strftime('%Y') for d in dates]
    else:  # monthly
        dates = [datetime(today.year, i, 1).date() for i in range(1, 13)]
        labels = [d.strftime('%b') for d in dates]

    values = []
    for d in dates:
        if filter == 'daily':
            end = d + timedelta(days=1)
        elif filter == 'monthly':
            end = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        else:
            end = d.replace(year=d.year + 1)

        total = MonthlyExpense.objects.filter(date__gte=d, date__lt=end).aggregate(s=Sum('amount'))['s'] or 0
        values.append(round(total, 2))

    return JsonResponse({'labels': labels, 'data': values})


@login_required
def export_expense_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="total_expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Company', 'Employee', 'Date', 'Expense Type', 'Amount','Amount Type', 'Description'])

    for e in MonthlyExpense.objects.select_related('company', 'employee'):
        writer.writerow([
            e.company.name,
            e.employee.name if e.employee else "N/A",
            e.date,
            e.expense_type,
            e.amount_type,
            e.amount,
            e.description
        ])

    return response

# Vendor Payments 
'''
@login_required
def add_vendor_payments(request):
    if request.method == 'POST':
        form = MonthlyVendorPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_vendor_payments')
    else:
        form = MonthlyVendorPaymentForm()
    return render(request, 'add_vendor_payments.html', {'form': form})
'''

# spp/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MonthlyVendorPaymentForm
from .models import MonthlyVendorPayment, VendorPaymentEntry
from core.models import PaymentMode


from collections import defaultdict
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.http import JsonResponse, HttpResponse
import csv

from .models import MonthlyVendorPayment  # Update if model is in a different app

@login_required
def vendor_payment_dashboard(request):
    # Breakdown by Vendor
    by_vendor = MonthlyVendorPayment.objects.values('vendor_name__supplier_name').annotate(total=Sum('amount'))

    # Breakdown by Payment Type
    payment_type_totals = defaultdict(float)
    for p in MonthlyVendorPayment.objects.prefetch_related('payments__payment_type'):
        for e in p.payments.all():
            payment_type_totals[e.payment_type.name] += float(e.amount)

    context = {
        'by_vendor': by_vendor,
        'by_payment_type': payment_type_totals.items(),
    }
    return render(request, 'vendor_payment_dashboard.html', context)


@login_required
def vendor_payment_chart_data(request):
    filter = request.GET.get('filter', 'monthly')
    today = now().date()

    if filter == 'daily':
        dates = [today - timedelta(days=i) for i in reversed(range(7))]
        labels = [d.strftime('%d %b') for d in dates]
    elif filter == 'yearly':
        dates = [datetime(today.year - i, 1, 1).date() for i in reversed(range(3))]
        labels = [d.strftime('%Y') for d in dates]
    else:  # monthly
        dates = [datetime(today.year, i, 1).date() for i in range(1, 13)]
        labels = [d.strftime('%b') for d in dates]

    values = []
    for d in dates:
        if filter == 'daily':
            end = d + timedelta(days=1)
        elif filter == 'monthly':
            end = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        else:
            end = d.replace(year=d.year + 1)

        total = MonthlyVendorPayment.objects.filter(date__gte=d, date__lt=end).aggregate(s=Sum('amount'))['s'] or 0
        values.append(round(total, 2))

    return JsonResponse({'labels': labels, 'data': values})


@login_required
def export_vendor_payment_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendor_payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Vendor Name', 'Date', 'Amount', 'Description', 'Payment Summary'])

    for v in MonthlyVendorPayment.objects.prefetch_related('payments__payment_type'):
        writer.writerow([
            v.vendor_name.name,
            v.date,
            v.amount,
            v.description,
            v.payment_summary()
        ])

    return response


@login_required
def manage_vendor_payments(request):
    vendor_payments = MonthlyVendorPayment.objects.all()
    return render(request, 'manage_vendor_payments.html', {'vendor_payments': vendor_payments})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MonthlyVendorPayment, VendorPaymentEntry, PaymentMode
from .forms import MonthlyVendorPaymentForm

def add_vendor_payments(request):
    if request.method == 'POST':
        form = MonthlyVendorPaymentForm(request.POST)
        payments_data = []

        total_forms = int(request.POST.get('payments-TOTAL_FORMS', 0))
        for i in range(total_forms):
            payment_type = request.POST.get(f'payments-{i}-payment_type')
            amount = request.POST.get(f'payments-{i}-amount')
            if payment_type and amount:
                payments_data.append({
                    'type': payment_type,
                    'amount': float(amount),
                })

        if form.is_valid():
            monthly_payment = form.save(commit=False)
            total_amount = float(monthly_payment.amount)
            total_paid = sum(p['amount'] for p in payments_data)

            #monthly_payment.total_payments = total_paid
            monthly_payment.save()

            for p in payments_data:
                payment_mode_obj, _ = PaymentMode.objects.get_or_create(name=p['type'])
                VendorPaymentEntry.objects.create(
                    vendor_payment=monthly_payment,
                    payment_type=payment_mode_obj,
                    amount=p['amount']
                )

            messages.success(request, "Vendor payment saved successfully.")
            return redirect('manage_vendor_payments')  # 🔁 Redirect works here!
        else:
            messages.error(request, "Please fix the form errors below.")
    else:
        form = MonthlyVendorPaymentForm()

    return render(request, 'add_vendor_payments.html', {
        'vendor_payment_form': form
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import MonthlySale
from .forms import MonthlySaleForm
from django.forms import modelform_factory
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from .models import MonthlySale, PaymentEntry
from .forms import MonthlySaleForm

@login_required
@transaction.atomic
def edit_sales(request, pk):
    sale = get_object_or_404(MonthlySale, pk=pk)
    if request.method == 'POST':
        form = MonthlySaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()

            # Clear existing payments
            sale.payments.all().delete()

            total_forms = int(request.POST.get('payments-TOTAL_FORMS', 0))
            for i in range(total_forms):
                p_type = request.POST.get(f'payments-{i}-payment_type')
                p_amount = request.POST.get(f'payments-{i}-amount')
                if p_type and p_amount:
                    PaymentEntry.objects.create(
                        sale=sale,
                        payment_type=p_type,
                        amount=p_amount
                    )
            return redirect('manage_sales')
    else:
        form = MonthlySaleForm(instance=sale)
        payments = sale.payments.all()
        payments_json = json.dumps(
            [{'type': p.payment_type, 'amount': float(p.amount)} for p in payments]
        )

    return render(request, 'edit_sales.html', {
        'sale_form': form,
        'sale': sale,
        'payments_json': payments_json,
    })

@login_required
def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_summary.csv"'

    writer = csv.writer(response)
    writer.writerow(['Invoice No', 'Date', 'Product', 'Company', 'Amount', 'Payment Status'])

    for sale in MonthlySale.objects.all():
        writer.writerow([
            sale.invoice_number,
            sale.date.strftime("%Y-%m-%d"),
            sale.product.name,
            sale.company.name,
            f"{sale.amount:.2f}",
            sale.payment_message()
        ])

    return response

@login_required
def delete_sales(request, pk):
    sale = get_object_or_404(MonthlySale, pk=pk)
    sale.delete()
    return redirect('manage_sales')


from .models import MonthlyExpense
from .forms import MonthlyExpenseForm

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(MonthlyExpense, pk=pk)
    if request.method == 'POST':
        form = MonthlyExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('manage_expenses')
        else:
            print(form.errors)
    else:
        form = MonthlyExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(MonthlyExpense, pk=pk)
    expense.delete()
    return redirect('manage_expenses')

from .models import MonthlyVendorPayment
from .forms import MonthlyVendorPaymentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import MonthlyVendorPayment, VendorPaymentEntry, PaymentMode
from .forms import MonthlyVendorPaymentForm

def edit_vendor_payment(request, pk):
    vendor_payment = get_object_or_404(MonthlyVendorPayment, pk=pk)

    if request.method == 'POST':
        form = MonthlyVendorPaymentForm(request.POST, instance=vendor_payment)
        payments_data = []

        total_forms = int(request.POST.get('payments-TOTAL_FORMS', 0))
        for i in range(total_forms):
            payment_type = request.POST.get(f'payments-{i}-payment_type')
            amount = request.POST.get(f'payments-{i}-amount')
            if payment_type and amount:
                payments_data.append({
                    'type': payment_type,
                    'amount': float(amount),
                })

        if form.is_valid():
            monthly_payment = form.save(commit=False)
            total_amount = float(monthly_payment.amount)
            total_paid = sum(p['amount'] for p in payments_data)

            #monthly_payment.total_payments = total_paid
            monthly_payment.save()

            # ❌ Delete existing payment entries
            VendorPaymentEntry.objects.filter(vendor_payment=monthly_payment).delete()

            # ✅ Recreate entries
            for p in payments_data:
                payment_mode_obj, _ = PaymentMode.objects.get_or_create(name=p['type'])
                VendorPaymentEntry.objects.create(
                    vendor_payment=monthly_payment,
                    payment_type=payment_mode_obj,
                    amount=p['amount']
                )

            messages.success(request, "Vendor payment updated successfully.")
            return redirect('manage_vendor_payments')
        else:
            messages.error(request, "Please fix the form errors below.")
    else:
        form = MonthlyVendorPaymentForm(instance=vendor_payment)
        existing_entries = VendorPaymentEntry.objects.filter(vendor_payment=vendor_payment)
        payments_json = [
            {'type': e.payment_type.name, 'amount': float(e.amount)}
            for e in existing_entries
        ]

    return render(request, 'edit_vendor_payments.html', {
        'vendor_payment_form': form,
        'existing_payments': payments_json
    })

@login_required
def delete_vendor_payment(request, pk):
    payment = get_object_or_404(MonthlyVendorPayment, pk=pk)
    payment.delete()
    return redirect('manage_vendor_payments')



from django.db.models import Sum
from datetime import datetime


@login_required
def monthly_sales(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    sales = MonthlySale.objects.filter(date__month=current_month, date__year=current_year)
    total_sales = sales.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'monthly_sales.html', {'sales': sales, 'total_sales': total_sales})
