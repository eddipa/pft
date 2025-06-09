from django.urls import path, include

from .views import dashboard, analysis_view
from .views import (
    transaction_list,
    transaction_export_csv,
    add_transaction, 
	edit_transaction, 
	delete_transaction)
from .views import (
    category_list,
    create_category,
    edit_category,
    delete_category,
)
from .views import (
    account_list,
    create_account,
    edit_account,
    delete_account,
)


app_name = 'finance'

urlpatterns = [
	path('', dashboard, name='dashboard'),
    path('analysis/', analysis_view, name='analysis'),

    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/export/', transaction_export_csv, name='transaction_export_csv'),
	path('add-transaction/', add_transaction, name='add_transaction'),
	# there is no view transaction view
	path('transaction/<int:pk>', edit_transaction, name='edit_transaction'),
	path('transaction/<int:pk>/delete/', delete_transaction, name='delete_transaction'),

	path('categories/', category_list, name='category_list'),
    path('categories/new/', create_category, name='create_category'),
    path('categories/<int:pk>/edit/', edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', delete_category, name='delete_category'),

    path('accounts/', account_list, name='account_list'),
    path('accounts/new/', create_account, name='create_account'),
    path('accounts/<int:pk>/edit/', edit_account, name='edit_account'),
    path('accounts/<int:pk>/delete/', delete_account, name='delete_account'),
]