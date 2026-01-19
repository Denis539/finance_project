from django import forms
from .models import Transaction
from .models import Category, FinancialGoal
from django.db.models import Q

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full border-2 border-black p-2'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full border-2 border-black p-2', 'placeholder': '0.00'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = Category.objects.filter(
                Q(user=user) | Q(user__isnull=True)
            ).order_by('name')
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_income']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border-2 border-black p-2', 'placeholder': 'Например: Продукты'}),
            'is_income': forms.CheckboxInput(attrs={'class': 'w-6 h-6 border-2 border-black'}),
        }

class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['title', 'target_amount']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border-2 border-black p-2', 'placeholder': 'Например: Наушники'}),
            'target_amount': forms.NumberInput(attrs={'class': 'w-full border-2 border-black p-2', 'placeholder': '10000'}),
            'deadline': forms.DateInput(attrs={'class': 'w-full border-2 border-black p-2', 'type': 'date'}),
        }