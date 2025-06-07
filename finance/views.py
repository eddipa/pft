from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, TransactionCategory, TransactionAccount
from datetime import date
from .forms import TransactionForm


@login_required
def dashboard(request):
    user = request.user

    today = date.today()
    month_start = date(today.year, today.month, 1)

    # Total balance by all accounts
    accounts = TransactionAccount.objects.filter(user=user)
    # ToDo: Assume accounts have a balance field (optional)

    # Summary by entry type
    monthly_transactions = Transaction.objects.filter(user=user, date__gte=month_start)
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
            return redirect('finance:dashboard')  # Redirect after saving
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'finance/add_transaction.html', {'form': form})
