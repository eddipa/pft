from django import forms
from .models import Transaction, TransactionCategory, TransactionAccount

FONT_AWESOME_ICONS = [
    ('', 'Select an icon...'),
    ('fa-solid fa-utensils', '🍴 Utensils'),
    ('fa-solid fa-car', '🚗 Car'),
    ('fa-solid fa-house', '🏠 House'),
    ('fa-solid fa-credit-card', '💳 Credit Card'),
    ('fa-solid fa-bolt', '⚡ Electricity'),
    ('fa-solid fa-basket-shopping', '🛒 Shopping'),
    ('fa-solid fa-heart-pulse', '❤️ Health'),
    ('fa-solid fa-graduation-cap', '🎓 Education'),
]

class ColorPickerWidget(forms.TextInput):
    input_type = 'color'

class IconSelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = str(option_value)
        selected_html = ' selected="selected"' if option_value in selected_choices else ''
        return f'<option value="{option_value}"{selected_html} data-icon="{option_value}">{option_label}</option>'

class IconPickerWidget(forms.TextInput):
    template_name = 'finance/widgets/icon_picker.html'

    class Media:
        css = {
            'all': ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css']
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'entry_type', 'category', 'transaction_account', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pull the user from passed-in kwargs
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if user:
            self.fields['category'].queryset = TransactionCategory.objects.filter(user=user)
            self.fields['transaction_account'].queryset = TransactionAccount.objects.filter(user=user)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['name', 'color', 'icon', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'color': ColorPickerWidget(),
            'icon': IconSelect(choices=FONT_AWESOME_ICONS),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pull the user from passed-in kwargs
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if user:
            self.fields['name' ,'description'].queryset = TransactionCategory.objects.filter(user=user)

    def clean_name(self):
        name = self.cleaned_data['name']
        if TransactionCategory.objects.filter(name__iexact=name, user=self.user).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("You already have a category with this name.")
        return name

class TransactionAccountForm(forms.ModelForm):
    class Meta:
        model = TransactionAccount
        fields = ['name', 'color', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'color': ColorPickerWidget(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pull the user from passed-in kwargs
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if user:
            self.fields['name' ,'description'].queryset = TransactionAccount.objects.filter(user=user)

    def clean_name(self):
        name = self.cleaned_data['name']
        if TransactionAccount.objects.filter(name__iexact=name, user=self.user).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("You already have an account with this name.")
        return name

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = '__all__'
        widgets = {
            'color': ColorPickerWidget(),
            'icon': IconPickerWidget(),
        }

class AccountAdminForm(forms.ModelForm):
    class Meta:
        model = TransactionAccount
        fields = '__all__'
        widgets = {
            'color': ColorPickerWidget(),
        }
