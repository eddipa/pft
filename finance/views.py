from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now

from .models import Transaction, TransactionCategory, TransactionAccount
from .forms import TransactionForm, TransactionCategoryForm

from .accounts_views import *
from .categories_views import *


@login_required
def dashboard(request):
    user = request.user

    today = date.today()
    month_start = date(today.year, today.month, 1)

    # Total balance by all accounts
    accounts = TransactionAccount.objects.filter(user=user)
    # ToDo: Assume accounts have a balance field (optional)

    user = request.user

    # Get selected month from GET parameter (default: current month)
    month_str = request.GET.get("month")
    if month_str:
        try:
            selected_date = datetime.strptime(month_str, "%Y-%m")
        except ValueError:
            selected_date = now().date()
    else:
        selected_date = now().date()

    # Start and end of selected month
    month_start = selected_date.replace(day=1)
    if month_start.month == 12:
        month_end = month_start.replace(year=month_start.year+1, month=1)
    else:
        month_end = month_start.replace(month=month_start.month+1)

    # Filter transactions for selected month
    monthly_transactions = Transaction.objects.filter(
        user=user,
        date__gte=month_start,
        date__lt=month_end
    )

    income = monthly_transactions.filter(entry_type="IN").aggregate(Sum("amount"))["amount__sum"] or 0
    expense = monthly_transactions.filter(entry_type="EX").aggregate(Sum("amount"))["amount__sum"] or 0
    net = income - expense

    # Recent transactions
    recent = monthly_transactions.order_by("-date")[:5]

    context = {
        "accounts": accounts,
        "income": income,
        "expense": expense,
        "net": net,
        "recent_transactions": recent,
        "selected_month": month_start,
        "current_month": now().date(),
    }

    return render(request, "finance/dashboard.html", context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully.")
            return redirect('finance:dashboard')  # Redirect after saving
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'finance/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect('finance:dashboard')
    else:
        form = TransactionForm(instance=transaction, user=request.user)

    return render(request, 'finance/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
        return redirect('finance:dashboard')

    return render(request, 'finance/delete_transaction.html', {'transaction': transaction})

