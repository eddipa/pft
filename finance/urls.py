from django.urls import path, include

from .views import dashboard, add_transaction, edit_transaction, delete_transaction


app_name = 'finance'

urlpatterns = [
	path('', dashboard, name='dashboard'),
	path('add-transaction/', add_transaction, name='add_transaction'),
	# there is no view transaction view
	path('transaction/<int:pk>', edit_transaction, name='edit_transaction'),
	path('transaction/<int:pk>/delete/', delete_transaction, name='delete_transaction'),
]