from django.contrib import admin

from .models import TransactionCategory, TransactionAccount, Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'entry_type', 'category', 'transaction_account', 'date')
    list_filter = ('entry_type', 'date', 'user')
    search_fields = ('description', 'user__username', 'category__name')


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'description', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user', 'name',)


@admin.register(TransactionAccount)
class TransactionAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)