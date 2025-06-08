from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TransactionAccount
from .forms import TransactionAccountForm

@login_required
def account_list(request):
    accounts = TransactionAccount.objects.filter(user=request.user)
    return render(request, 'finance/accounts/account_list.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = TransactionAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('finance:account_list')
    else:
        form = TransactionAccountForm()
    return render(request, 'finance/accounts/account_form.html', {'form': form, 'title': 'Add Account'})

@login_required
def edit_account(request, pk):
    account = get_object_or_404(TransactionAccount, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('finance:account_list')
    else:
        form = TransactionAccountForm(instance=account)
    return render(request, 'finance/accounts/account_form.html', {'form': form, 'title': 'Edit Account'})

@login_required
def delete_account(request, pk):
    account = get_object_or_404(TransactionAccount, pk=pk, user=request.user)

    if account.is_default:
        messages.error(request, "You cannot delete the default account.")
        return redirect('finance:account_list')

    transactions_exist = account.account_transactions.exists()
    other_accounts = TransactionAccount.objects.filter(user=request.user).exclude(pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        target_account_id = request.POST.get('target_account')

        if action == 'delete_all':
            account.account_transactions.all().delete()
        elif action == 'move' and target_account_id:
            target = get_object_or_404(TransactionAccount, pk=target_account_id, user=request.user)
            account.account_transactions.update(transaction_account=target)

        account.delete()
        return redirect('finance:account_list')

    return render(request, 'finance/accounts/account_confirm_delete.html', {
        'account': account,
        'transactions_exist': transactions_exist,
        'other_accounts': other_accounts,
    })