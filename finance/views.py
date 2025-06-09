from datetime import date, datetime, timedelta
import json
import csv
from collections import defaultdict

from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum ,Q
from django.core.paginator import Paginator
from django.utils.timezone import now

from xhtml2pdf import pisa

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
    percent_spent = (expense / income * 100) if income > 0 else 0
    percent_saved = 100 - percent_spent if income > 0 else 0

    # Find most spent category
    top_category = (
        monthly_transactions.filter(entry_type="EX")
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
        .first()
    )

    # Recent transactions
    recent = monthly_transactions.order_by("-date")[:7]

    context = {
        "accounts": accounts,
        "income": income,
        "expense": expense,
        "net": net,
        "recent_transactions": recent,
        "selected_month": month_start,
        "current_month": now().date(),
        "percent_spent": round(percent_spent, 1),
        "percent_saved": round(percent_saved, 1),
        "top_category": top_category,
    }

    return render(request, "finance/dashboard.html", context)

@login_required
def analysis_view(request):
    user = request.user
    today = now()

    # Get query parameters
    selected_month = request.GET.get('month')
    selected_account = request.GET.get('account')

    # Month options: last 6 months
    month_options = [(today - timedelta(days=30 * i)).strftime('%Y-%m') for i in range(6)]
    account_options = TransactionAccount.objects.filter(user=user)

    # Filter base queryset
    queryset = Transaction.objects.filter(user=user)

    if selected_month:
        year, month = map(int, selected_month.split('-'))
        queryset = queryset.filter(date__year=year, date__month=month)
    else:
        selected_month = today.strftime('%Y-%m')  # default to current month
        queryset = queryset.filter(date__year=today.year, date__month=today.month)

    if selected_account and selected_account != 'all':
        queryset = queryset.filter(transaction_account__id=selected_account)

    # Get all user categories
    all_categories = TransactionCategory.objects.filter(user=user)

    # Get expense sums for current filter
    expense_totals = (
        queryset.filter(entry_type='EX')
        .values('category')
        .annotate(total=Sum('amount'))
    )

    # Build a dict of {category_id: total}
    expense_dict = {entry['category']: float(entry['total']) for entry in expense_totals}

    # Combine with all categories (add 0 if missing)
    chart_labels = []
    chart_values = []

    for cat in all_categories:
        chart_labels.append(cat.name)
        chart_values.append(expense_dict.get(cat.id, 0.0))

    # print("chart_labels =", chart_labels)
    # print("chart_values =", chart_values)


    # Find the top category based on the highest value
    if chart_values:
        max_index = chart_values.index(max(chart_values))
        top_category = chart_labels[max_index] if chart_values[max_index] > 0 else "N/A"
    else:
        top_category = "N/A"

    # Bar chart: income/expense over last 6 months
    six_months_ago = today - timedelta(days=180)
    raw = (
        Transaction.objects.filter(user=user, date__gte=six_months_ago)
        .extra(select={'month': "strftime('%%Y-%%m', date)"})
        .values('month', 'entry_type')
        .annotate(total=Sum('amount'))
    )

    # Build a dictionary like {month: {'income': 0, 'expense': 0}}
    monthly_data = defaultdict(lambda: {'IN': 0, 'EX': 0})
    for item in raw:
        monthly_data[item['month']][item['entry_type']] = float(item['total'])
    # Sort by month and extract values
    chart_months = sorted(monthly_data.keys())
    income_data = [monthly_data[m]['IN'] for m in chart_months]
    expense_data = [monthly_data[m]['EX'] for m in chart_months]

    # print("chart_months =", chart_months)
    # print("income_data =", income_data)
    # print("expense_data =", expense_data)

    # Summary
    net_savings = queryset.filter(entry_type='IN').aggregate(total=Sum('amount'))['total'] or 0
    net_savings -= queryset.filter(entry_type='EX').aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_months': chart_months,
        'income_data': income_data,
        'expense_data': expense_data,
        'month_options': month_options,
        'account_options': account_options,
        'selected_month': selected_month,
        'selected_account': selected_account,
        'net_savings': round(net_savings, 2),
        'top_category': top_category,
    }

    return render(request, 'finance/analysis.html', context)

@login_required
def export_analysis_pdf(request):
    if request.method == 'POST':
        net_savings = request.POST.get('net_savings', 'N/A')
        top_category = request.POST.get('top_category', 'N/A')
        chart_pie = request.POST.get('chart_pie', '')
        chart_bar = request.POST.get('chart_bar', '')
        selected_month = request.POST.get('month', '')
        account_name = request.POST.get('account_name', 'All')

        # Parse selected month
        try:
            year, month = map(int, selected_month.split('-'))
        except:
            year, month = now().year, now().month

        # Filter transactions
        queryset = Transaction.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        ).select_related('category', 'transaction_account')

        if account_name != 'All':
            queryset = queryset.filter(transaction_account__name=account_name)

        transactions = queryset.order_by('-date')
        print(top_category)
        # Render the template
        template = get_template('finance/analysis_pdf.html')
        html = template.render({
            'net_savings': net_savings,
            'top_category': top_category,
            'chart_pie': chart_pie,
            'chart_bar': chart_bar,
            'selected_month': selected_month,
            'selected_account': account_name,
            'transactions': transactions,
            'generated_on': now(),
        })


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="analysis_report.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response
    else:
        return HttpResponse("Invalid request", status=400)

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)

    # Get parameters
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    account_id = request.GET.get('account', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    # Apply filters
    if query:
        transactions = transactions.filter(description__icontains=query)

    if category_id.isdigit():
        transactions = transactions.filter(category_id=int(category_id))

    if account_id.isdigit():
        transactions = transactions.filter(transaction_account_id=int(account_id))

     # Date filtering
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            transactions = transactions.filter(date__gte=start)
        except ValueError:
            pass

    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            transactions = transactions.filter(date__lte=end)
        except ValueError:
            pass

    categories = TransactionCategory.objects.filter(user=request.user)
    accounts = TransactionAccount.objects.filter(user=request.user)

    # pagination
    paginator = Paginator(transactions, 10) 
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    return render(request, 'finance/transaction_list.html', {
        'transactions': transactions,
        'categories': categories,
        'accounts': accounts,
        'query': query,
        'selected_category': int(category_id) if category_id.isdigit() else None,
        'selected_account': int(account_id) if account_id.isdigit() else None,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def transaction_export_csv(request):
    transactions = Transaction.objects.filter(user=request.user)

    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    account_id = request.GET.get('account', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    if query:
        transactions = transactions.filter(description__icontains=query)
    if category_id.isdigit():
        transactions = transactions.filter(category_id=int(category_id))
    if account_id.isdigit():
        transactions = transactions.filter(transaction_account_id=int(account_id))
    if start_date:
        try:
            transactions = transactions.filter(date__gte=start_date)
        except:
            pass
    if end_date:
        try:
            transactions = transactions.filter(date__lte=end_date)
        except:
            pass

    # Create CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Amount', 'Category', 'Account'])

    for t in transactions:
        writer.writerow([
            t.date, t.description, t.amount,
            t.category.name if t.category else '',
            t.transaction_account.name if t.transaction_account else ''
        ])

    return response

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

