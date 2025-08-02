from django.contrib import admin
from .models import (
    TaskImportance, ProjectStatus, TaskStatus, TransactionType,
    Segment, PaymentMode, EntryType, ExpenseType, VoucherType,
    EmployeePaymentType, LeaveType
)

admin.site.register(TaskImportance)
admin.site.register(ProjectStatus)
admin.site.register(TaskStatus)
admin.site.register(TransactionType)
admin.site.register(Segment)
admin.site.register(PaymentMode)
admin.site.register(EntryType)
admin.site.register(ExpenseType)
admin.site.register(VoucherType)
admin.site.register(EmployeePaymentType)
admin.site.register(LeaveType)
