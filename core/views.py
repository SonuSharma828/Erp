from django.shortcuts import render, redirect
from .models import *
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect





MODEL_MAP = {
    'company': Company,
    'AmountType': AmountType,
    'task-importance': TaskImportance,
    'project-status': ProjectStatus,
    'project-type': ProjectType,
    'task-status': TaskStatus,
    'photo-id-type': PhotoIdType,
    'transaction-type': TransactionType,
    'segment': Segment,
    'payment-mode': PaymentMode,
    'entry-type': EntryType,
    'expense-type': ExpenseType,
    'voucher-type': VoucherType,
    'employee-payment-type': EmployeePaymentType,
    'leave-type': LeaveType,
    'Spp-Transaction-Type': SppTransactionType,
    'Attendance-Status-Type': AttendanceStatusType,
    'Knw-Group-Type': KnwGroupType,
    'Knw-Sub-Group-Type': KnwSubGroupType,
}

LABELS = {
    'company':"Company",
    'AmountType': "Amount Type",
    'task-importance': "Task Importance",
    'project-status': "Project Status",
    'project-type': "Project Type",
    'task-status': "Task Status",
    'photo-id-type': "Photo Id Type",
    'transaction-type': "Transaction Type",
    'segment': "Segment",
    'payment-mode': "Payment Mode",
    'entry-type': "Entry Type",
    'expense-type': "Expense Type",
    'voucher-type': "Voucher Type",
    'employee-payment-type': "Employee Payment Type",
    'leave-type': "Leave Type",
    'Spp-Transaction-Type': "SPP Transaction Type",
    'Attendance-Status-Type': "Attendance Status Type",
    'Knw-Group-Type': "Knw Group Type",
    'Knw-Sub-Group-Type': "Knw Sub Group Type",
}

def manage_dropdowns(request):
    if request.method == 'POST':
        model_key = request.POST.get('model')
        name = request.POST.get('name')
        Model = MODEL_MAP.get(model_key)
        if Model and name:
            Model.objects.create(name=name)
            return redirect('manage_dropdowns')

    items_dict = {key: MODEL_MAP[key].objects.all() for key in MODEL_MAP}

    return render(request, 'manage_dropdowns.html', {
        'dropdowns': LABELS,
        'items_dict': items_dict,
    })


def update_field(request, model_key, pk):
    Model = MODEL_MAP.get(model_key)
    if not Model:
        return redirect('manage_dropdowns')

    instance = get_object_or_404(Model, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            instance.name = name
            instance.save()
            return redirect('manage_dropdowns')

    return render(request, 'update_field.html', {
        'field': instance,
        'model_key': model_key,
        'label': LABELS.get(model_key, model_key),
    })




def delete_field(request, model_key, pk):
    Model = MODEL_MAP.get(model_key)
    if not Model:
        return redirect('manage_dropdowns')

    instance = get_object_or_404(Model, pk=pk)
    instance.delete()
    return redirect('manage_dropdowns')

