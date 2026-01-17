from django.contrib import admin
from .models import Category, FinancialGoal, Transaction

admin.site.register(Category)
admin.site.register(FinancialGoal)
admin.site.register(Transaction)