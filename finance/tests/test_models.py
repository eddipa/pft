from django.test import TestCase
from finance.models import Transaction, Category, Account
from django.contrib.auth import get_user_model

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass')
        self.account = Account.objects.create(name='Bank', user=self.user)
        self.category = Category.objects.create(name='Food', user=self.user)

    def test_create_transaction(self):
        tx = Transaction.objects.create(
            user=self.user,
            transaction_account=self.account,
            category=self.category,
            amount=50,
            entry_type='IN',
            date='2025-06-09'
        )
        self.assertEqual(tx.amount, 50)
        self.assertEqual(tx.entry_type, 'IN')
