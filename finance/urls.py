from django.urls import path, include

from .views import dashboard
from .views import (add_transaction, 
	edit_transaction, 
	delete_transaction)
from .views import (
    category_list,
    create_category,
    edit_category,
    delete_category,
)


app_name = 'finance'

urlpatterns = [
	path('', dashboard, name='dashboard'),

	path('add-transaction/', add_transaction, name='add_transaction'),
	# there is no view transaction view
	path('transaction/<int:pk>', edit_transaction, name='edit_transaction'),
	path('transaction/<int:pk>/delete/', delete_transaction, name='delete_transaction'),

	path('categories/', category_list, name='category_list'),
    path('categories/new/', create_category, name='create_category'),
    path('categories/<int:pk>/edit/', edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', delete_category, name='delete_category'),
]