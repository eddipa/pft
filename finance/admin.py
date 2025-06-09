from django.contrib import admin

from .models import TransactionCategory, TransactionAccount, Transaction
from .forms import CategoryAdminForm, AccountAdminForm

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'entry_type', 'category', 'transaction_account', 'date')
    list_filter = ('entry_type', 'date', 'user')
    search_fields = ('description', 'user__username', 'category__name')


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'user', 'description', 'color', 'icon', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user', 'name',)


@admin.register(TransactionAccount)
class TransactionAccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = ('user', 'name', 'color', 'description', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)