from django.contrib import admin
from .models import Empdata, Department, Report
from HRM.models import Department


@admin.register(Empdata)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'salary', 'department', 'active_status', 'payroll_status')
    search_fields = ('name', 'email')
    list_filter = ('active', 'in_payroll', 'department')

    def active_status(self, obj):
        return "✅" if obj.active else "❌"
    active_status.short_description = 'Active'

    def payroll_status(self, obj):
        return "✅" if obj.in_payroll else "❌"
    payroll_status.short_description = 'In Payroll'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__name')
    list_filter = ('created_at',)




from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'leave_type', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'leave_type', 'start_date']
    search_fields = ['user__username', 'reason']



