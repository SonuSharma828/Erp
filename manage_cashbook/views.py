from django.shortcuts import render, redirect, get_object_or_404
from .models import CashbookEntry
from .forms import CashbookEntryForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from core.models import PaymentMode,Segment,EntryType
'''
@login_required
def cashbook_list(request):
    entries = CashbookEntry.objects.all().order_by('-entry_date')

    amount_in = CashbookEntry.objects.filter(entry_type='In').aggregate(total_in=Sum('amount'))['total_in'] or 0
    amount_out = CashbookEntry.objects.filter(entry_type='Out').aggregate(total_out=Sum('amount'))['total_out'] or 0
    types = EntryType.objects.all()
    segments = Segment.objects.all()
    context = {
        'entries': entries,
        'amount_in': amount_in,
        'amount_out': amount_out,
        'segments': segments,
        'types': types,
    }
    return render(request, 'cashbook_list.html', context)
'''

from django.core.paginator import Paginator

@login_required
def cashbook_list(request):
    entries = CashbookEntry.objects.all().order_by('-entry_date')

    # Apply pagination
    paginator = Paginator(entries, 10)  # Show 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    amount_in = CashbookEntry.objects.filter(entry_type='In').aggregate(total_in=Sum('amount'))['total_in'] or 0
    amount_out = CashbookEntry.objects.filter(entry_type='Out').aggregate(total_out=Sum('amount'))['total_out'] or 0
    types = EntryType.objects.all()
    segments = Segment.objects.all()

    context = {
        'page_obj': page_obj,
        'entries': page_obj.object_list,
        'amount_in': amount_in,
        'amount_out': amount_out,
        'segments': segments,
        'types': types,
    }
    return render(request, 'cashbook_list.html', context)

@login_required
def add_cashbook_entry(request):
    if request.method == 'POST':
        form = CashbookEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user
            entry.save()
            return redirect('cashbook_list')
    else:
        form = CashbookEntryForm()
    return render(request, 'add_cashbook.html', {'form': form})

@login_required
def edit_cashbook_entry(request, entry_id):
    entry = get_object_or_404(CashbookEntry, id=entry_id)
    if request.method == 'POST':
        form = CashbookEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('cashbook_list')
    else:
        form = CashbookEntryForm(instance=entry)
    return render(request, 'edit_cashbook.html', {'form': form, 'entry': entry})

@login_required
def delete_cashbook_entry(request, entry_id):
    entry = get_object_or_404(CashbookEntry, id=entry_id)
    entry.delete()
    return redirect('cashbook_list')
