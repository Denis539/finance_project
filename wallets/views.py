from django.shortcuts import render
from .models import FinancialGoal, Transaction

def index(request):
    # Считаем количество записей в базе для статистики
    goals_count = FinancialGoal.objects.count()
    trans_count = Transaction.objects.count()
    
    context = {
        'goals_count': goals_count,
        'trans_count': trans_count,
    }
    return render(request, 'wallets/index.html', context)