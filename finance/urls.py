from django.urls import path, include

from .views import dashboard, add_transaction


app_name = 'finance'

urlpatterns = [
	path('', dashboard, name='dashboard'),
	path('add-transaction/', add_transaction, name='add_transaction'),
]