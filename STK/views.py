from django.shortcuts import render, get_object_or_404, redirect
from .models import STKUnit, STKCategory, STKStock, STKTake
from .forms import STKUnitForm, STKCategoryForm, STKStockForm, STKTakeForm
from django.contrib.auth.decorators import login_required
from core.models import TransactionType
from django.contrib.auth import get_user_model
# STK Units Views
'''
@login_required
def unit_list(request):
    units = STKUnit.objects.all()
    return render(request, 'unit_list.html', {'units': units})
'''

from django.core.paginator import Paginator

@login_required
def unit_list(request):
    units_list = STKUnit.objects.all().order_by('id')  # optional: add ordering
    paginator = Paginator(units_list, 10)  # Show 10 units per page

    page_number = request.GET.get('page')
    units = paginator.get_page(page_number)

    return render(request, 'unit_list.html', {'units': units})

@login_required
def unit_add(request):
    if request.method == 'POST':
        form = STKUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = STKUnitForm()
    return render(request, 'unit_form.html', {'form': form})

@login_required
def unit_edit(request, pk):
    unit = get_object_or_404(STKUnit, pk=pk)
    if request.method == 'POST':
        form = STKUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = STKUnitForm(instance=unit)
    return render(request, 'unit_form.html', {'form': form})

@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(STKUnit, pk=pk)
    unit.delete()
    return redirect('unit_list')

'''
# STK Categories Views
@login_required
def category_list(request):
    categories = STKCategory.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
'''

from django.core.paginator import Paginator

@login_required
def category_list(request):
    categories_all = STKCategory.objects.all().order_by('id')
    paginator = Paginator(categories_all, 10)  # 10 per page
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        form = STKCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = STKCategoryForm()
    return render(request, 'category_form.html', {'form': form})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(STKCategory, pk=pk)
    if request.method == 'POST':
        form = STKCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = STKCategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(STKCategory, pk=pk)
    category.delete()
    return redirect('category_list')

'''
# STK Stock Views
@login_required
def stock_list(request):
    stocks = STKStock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})
'''

from django.core.paginator import Paginator

@login_required
def stock_list(request):
    stock_qs = STKStock.objects.all().order_by('item_name')  # Optional: sorted
    paginator = Paginator(stock_qs, 10)  # Show 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'stock_list.html', {
        'stocks': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
    })


from .models import STKStock, STKStockHistory, STKTake
from django.utils import timezone

@login_required
def stock_add(request):
    if request.method == 'POST':
        form = STKStockForm(request.POST)
        if form.is_valid():
            new_item = form.cleaned_data
            existing_item = STKStock.objects.filter(item_name__iexact=new_item['item_name']).first()

            if existing_item:
                existing_item.quantity += new_item['quantity']
                existing_item.price = new_item['price']  # Optional: update latest price
                existing_item.save()

                # Record in stock history
                STKStockHistory.objects.create(
                    item=existing_item,
                    quantity_added=new_item['quantity'],
                    price_at_time=new_item['price'],
                    added_by=str(request.user)
                )

                # Also create a matching STKTake record
                STKTake.objects.create(
                    item=existing_item,
                    transaction_type='IN',
                    quantity=new_item['quantity'],
                    price=new_item['price'],
                    taken_by=str(request.user),
                    date=timezone.now(),
                    note='Auto-entry from stock_add'
                )
            else:
                saved_item = form.save()

                STKStockHistory.objects.create(
                    item=saved_item,
                    quantity_added=saved_item.quantity,
                    price_at_time=saved_item.price,
                    added_by=str(request.user)
                )

                # Create STKTake entry
                STKTake.objects.create(
                    item=saved_item,
                    transaction_type='IN',
                    quantity=saved_item.quantity,
                    price=saved_item.price,
                    taken_by=str(request.user),
                    date=timezone.now(),
                    note='Auto-entry from stock_add'
                )

            return redirect('stock_list')
    else:
        form = STKStockForm()
    return render(request, 'stock_form.html', {'form': form})

@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(STKStock, pk=pk)
    if request.method == 'POST':
        form = STKStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = STKStockForm(instance=stock)
    return render(request, 'stock_form.html', {'form': form})

@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(STKStock, pk=pk)
    stock.delete()
    return redirect('stock_list')

'''
# STK Take Views
@login_required
def take_list(request):
    takes = STKTake.objects.all()
    users = get_user_model().objects.filter(is_active=True)
    type = TransactionType.objects.all()
    return render(request, 'take_list.html', {'takes': takes,'users':users,'type':type,})
'''

from django.core.paginator import Paginator

@login_required
def take_list(request):
    takes = STKTake.objects.all()
    paginator = Paginator(takes, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users = get_user_model().objects.filter(is_active=True)
    type = TransactionType.objects.all()

    return render(request, 'take_list.html', {
        'page_obj': page_obj,
        'users': users,
        'type': type,
    })


from django.utils import timezone

@login_required
def take_add(request):
    if request.method == 'POST':
        form = STKTakeForm(request.POST)
        if form.is_valid():
            take = form.save(commit=False)
            stock_item = take.item
            transaction_type = take.transaction_type.name.strip().lower()
            user = str(request.user)

            # Try to find similar STKTake
            existing_take = STKTake.objects.filter(
                item=stock_item,
                taken_by=take.taken_by,
                transaction_type=take.transaction_type,
                note=take.note  # Optional filter, can remove for broader match
            ).first()

            # --- IN TRANSACTION ---
            if transaction_type == 'in':
                if STKStock.objects.filter(item_name__iexact=stock_item.item_name).exists():
                    stock = STKStock.objects.get(item_name__iexact=stock_item.item_name)
                    stock.quantity += take.quantity
                    if take.price:
                        stock.price = take.price
                    stock.save()
                else:
                    stock = STKStock.objects.create(
                        item_name=stock_item.item_name,
                        quantity=take.quantity,
                        price=take.price,
                        unit=stock_item.unit,
                        category=stock_item.category,
                        description=stock_item.description
                    )

                if existing_take:
                    existing_take.quantity += take.quantity
                    existing_take.price = take.price or existing_take.price
                    existing_take.date = timezone.now()
                    existing_take.save()
                else:
                    take.item = stock
                    take.save()

            # --- OUT TRANSACTION ---
            elif transaction_type == 'out':
                if stock_item.quantity < take.quantity:
                    form.add_error('quantity', 'Not enough stock available.')
                    return render(request, 'take_form.html', {'form': form})

                stock_item.quantity -= take.quantity
                stock_item.save()

                if existing_take:
                    existing_take.quantity += take.quantity
                    existing_take.date = timezone.now()
                    existing_take.save()
                else:
                    take.save()

            return redirect('take_list')
    else:
        form = STKTakeForm()
    return render(request, 'take_form.html', {'form': form})

@login_required
def take_edit(request, pk):
    take = get_object_or_404(STKTake, pk=pk)
    if request.method == 'POST':
        form = STKTakeForm(request.POST, instance=take)
        if form.is_valid():
            form.save()
            return redirect('take_list')
    else:
        form = STKTakeForm(instance=take)
    return render(request, 'take_form.html', {'form': form})

@login_required
def take_delete(request, pk):
    take = get_object_or_404(STKTake, pk=pk)
    take.delete()
    return redirect('take_list')



'''
@login_required
def stock_detail(request, pk):
    stock = get_object_or_404(STKStock, pk=pk)
    transactions = STKTake.objects.filter(item=stock).order_by('-date')
    return render(request, 'stock_detail.html', {
        'stock': stock,
        'transactions': transactions
    })

'''

@login_required
def stock_detail(request, pk):
    stock = get_object_or_404(STKStock, pk=pk)

    addition_history = stock.histories.all().order_by('-added_at')  # From STKStockHistory
    transaction_history = STKTake.objects.filter(item=stock).order_by('-date')  # From STKTake

    return render(request, 'stock_detail.html', {
        'stock': stock,
        'addition_history': addition_history,
        'transaction_history': transaction_history,
    })

