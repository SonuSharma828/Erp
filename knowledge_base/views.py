from django.shortcuts import render, redirect, get_object_or_404
from .models import KnowledgeBase
from .forms import KnowledgeBaseForm
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

@login_required
def knowledge_list(request):
    entry_list = KnowledgeBase.objects.all().order_by('-id')
    paginator = Paginator(entry_list, 20)  # 20 entries per page
    page = request.GET.get('page')
    entries = paginator.get_page(page)
    return render(request, 'knw_list.html', {'entries': entries})

'''
@login_required
def knowledge_list(request):
    entries = KnowledgeBase.objects.all()
    return render(request, 'knw_list.html', {'entries': entries})
'''
@login_required
def add_knowledge(request):
    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('knowledge_list')
    else:
        form = KnowledgeBaseForm()
    return render(request, 'add_knw_list.html', {'form': form})

@login_required
def edit_knowledge(request, pk):
    entry = get_object_or_404(KnowledgeBase, pk=pk)
    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('knowledge_list')
    else:
        form = KnowledgeBaseForm(instance=entry)
    return render(request, 'edit_knw_list.html', {'form': form})

@login_required
def delete_knowledge(request, pk):
    entry = get_object_or_404(KnowledgeBase, pk=pk)
    entry.delete()
    return redirect('knowledge_list')
