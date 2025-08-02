from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from finance.forms import ExpenseForm, IncomeForm, SalaryPaymentForm
from .models import Income, Expense, SalaryPayment

import csv
from django.http import HttpResponse

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance')  # Change as per your URL name
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance')  # Change as per your URL
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})


@login_required
def add_salary_payment(request):
    if request.method == 'POST':
        form = SalaryPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance')  # Adjust URL as needed
    else:
        form = SalaryPaymentForm()

    return render(request, 'add_salary_payment.html', {'form': form})

from django.shortcuts import render

from django.db.models import Sum
from datetime import datetime

@login_required
def finance_summary(request):
    # Default to current month
    start_date = datetime.now().replace(day=1)
    end_date = datetime.now()

    # If a date range is specified via GET request
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d')

    total_income = Income.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    total_salary = SalaryPayment.objects.filter(payment_date__range=[start_date, end_date]).aggregate(Sum('salary_amount'))['salary_amount__sum'] or 0

    profit_loss = total_income - total_expense

    return render(request, 'finance_summary.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'total_salary': total_salary,
        'profit_loss': profit_loss,
        'start_date': start_date,
        'end_date': end_date,
    })



@login_required
def export_finance_csv(request):
    # Get the date range (if provided)
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Filter data based on the date range
    income_data = Income.objects.filter(date__range=[start_date, end_date])
    expense_data = Expense.objects.filter(date__range=[start_date, end_date])
    salary_data = SalaryPayment.objects.filter(payment_date__range=[start_date, end_date])

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="finance_summary.csv"'
    writer = csv.writer(response)

    # Write headers for CSV
    writer.writerow(['Income', 'Amount (₹)', 'Date'])
    for income in income_data:
        writer.writerow([income.description, income.amount, income.date])

    writer.writerow([])  # Empty row to separate sections

    writer.writerow(['Expense', 'Amount (₹)', 'Date'])
    for expense in expense_data:
        writer.writerow([expense.description, expense.amount, expense.date])

    writer.writerow([])  # Empty row to separate sections

    writer.writerow(['Salary Payment', 'Amount (₹)', 'Payment Date'])
    for salary in salary_data:
        writer.writerow([salary.employee, salary.salary_amount, salary.payment_date])

    return response



from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from .models import Income, Expense, SalaryPayment

@login_required
def export_finance_pdf(request):
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    income_data = Income.objects.filter(date__range=[start_date, end_date])
    expense_data = Expense.objects.filter(date__range=[start_date, end_date])
    salary_data = SalaryPayment.objects.filter(payment_date__range=[start_date, end_date])

    total_income = sum([i.amount for i in income_data])
    total_expense = sum([e.amount for e in expense_data])
    total_salary = sum([s.salary_amount for s in salary_data])
    profit_loss = total_income - total_expense

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="finance_summary.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(f"<b>Finance Summary from {start_date} to {end_date}</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Summary
    summary_data = [
        ["Total Income", f"₹ {total_income}"],
        ["Total Expense", f"₹ {total_expense}"],
        ["Total Salary Paid", f"₹ {total_salary}"],
        ["Profit/Loss", f"₹ {profit_loss}"],
    ]
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT')
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # Income Data
    elements.append(Paragraph("Income Data:", styles['Heading2']))
    income_table_data = [["Description", "Amount (₹)", "Date"]]
    for i in income_data:
        income_table_data.append([i.description, f"{i.amount}", str(i.date)])
    income_table = Table(income_table_data, colWidths=[200, 100, 100])
    income_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(income_table)
    elements.append(Spacer(1, 20))

    # Expense Data
    elements.append(Paragraph("Expense Data:", styles['Heading2']))
    expense_table_data = [["Description", "Amount (₹)", "Date"]]
    for e in expense_data:
        expense_table_data.append([e.description, f"{e.amount}", str(e.date)])
    expense_table = Table(expense_table_data, colWidths=[200, 100, 100])
    expense_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(expense_table)
    elements.append(Spacer(1, 20))

    # Salary Data
    elements.append(Paragraph("Salary Payments:", styles['Heading2']))
    salary_table_data = [["Employee", "Amount (₹)", "Payment Date"]]
    for s in salary_data:
        salary_table_data.append([s.employee.name, f"{s.salary_amount}", str(s.payment_date)])
    salary_table = Table(salary_table_data, colWidths=[200, 100, 100])
    salary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(salary_table)

    # Build the PDF
    doc.build(elements)

    return response