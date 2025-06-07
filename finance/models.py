from django.db import models
from django.conf import settings
from django.utils import timezone


class TransactionAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transaction_accounts'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'name')  # Each user can have unique account names

    def __str__(self):
        return f"{self.name}"


class TransactionCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transaction_categories'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'name')  # Each user can have unique category names

    def __str__(self):
        return f"{self.name}"


class Transaction(models.Model):
	ENTRY_TYPE_CHOICES = [
	    ("IN", "Income"),
	    ("EX", "Expense"),
	    ("TR", "Transfer"),
	]

	amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
	date = models.DateField(default=timezone.now, null=False)
	entry_type = models.CharField(max_length=2, choices=ENTRY_TYPE_CHOICES)
	description = models.TextField(blank=True, null=True)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		related_name='user_transactions')
	category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, 
		null=True, blank=True, related_name='category_transactions')
	transaction_account = models.ForeignKey(TransactionAccount, on_delete=models.CASCADE, 
		related_name='account_transactions')

	def __str__(self):
		return f"{self.entry_type} - {self.amount} - {self.date}"