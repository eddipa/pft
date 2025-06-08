from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TransactionCategory
from .forms import TransactionCategoryForm


@login_required
def category_list(request):
    categories = TransactionCategory.objects.filter(user=request.user)
    return render(request, 'finance/categories/category_list.html', {'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = TransactionCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "New Category added successfully.")
            return redirect('finance:category_list')
    else:
        form = TransactionCategoryForm()
    return render(request, 'finance/categories/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(TransactionCategory, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category edited successfully.")
            return redirect('finance:category_list')
    else:
        form = TransactionCategoryForm(instance=category)
    return render(request, 'finance/categories/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(TransactionCategory, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('finance:category_list')
    return render(request, 'finance/categories/category_confirm_delete.html', {'category': category})