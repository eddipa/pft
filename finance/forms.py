from django import forms
from .models import Transaction, TransactionCategory, TransactionAccount


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'entry_type', 'category', 'transaction_account', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pull the user from passed-in kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = TransactionCategory.objects.filter(user=user)
            self.fields['transaction_account'].queryset = TransactionAccount.objects.filter(user=user)


class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pull the user from passed-in kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name' ,'description'].queryset = TransactionCategory.objects.filter(user=user)
