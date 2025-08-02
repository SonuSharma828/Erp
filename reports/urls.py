from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('report/', views.report_page, name='report_page'),
    path('export/pdf/', views.export_report_pdf, name='export_pdf'),  # PDF export
    path('export/excel/', views.export_report_excel, name='export_excel'),
]