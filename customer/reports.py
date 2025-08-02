# workorders/reports.py
from django.db.models import Count, Sum
from .models import WorkOrder

def employee_performance_report(start_date, end_date):
    return WorkOrder.objects.filter(
        scheduled_date__range=(start_date, end_date)
    ).values('assigned_to__user__username').annotate(
        total_orders=Count('id'),
        completed_orders=Count('id', filter=models.Q(status='COMPLETED')),
        completion_rate=100.0 * Count('id', filter=models.Q(status='COMPLETED')) / Count('id')
    ).order_by('-completion_rate')
