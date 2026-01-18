from django import forms
from .models import Transaction
from .models import Category, FinancialGoal


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full border-2 border-black p-2', 'placeholder': 'Например: Стипендия'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full border-2 border-black p-2', 'placeholder': '0.00'}),
        }
        
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