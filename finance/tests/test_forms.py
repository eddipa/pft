from finance.forms import TransactionForm
from django.test import TestCase
from finance.models import Account, Category
from django.contrib.auth import get_user_model

class TransactionFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='formtest@example.com', password='pass')
        self.account = Account.objects.create(name='Cash', user=self.user)
        self.category = Category.objects.create(name='Rent', user=self.user)

    def test_valid_form(self):
        form = TransactionForm(data={
            'amount': 100,
            'entry_type': 'OUT',
            'transaction_account': self.account.id,
            'category': self.category.id,
            'date': '2025-06-09'
        }, user=self.user)
        self.assertTrue(form.is_valid())
