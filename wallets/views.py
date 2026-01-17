from django.shortcuts import render
from .models import FinancialGoal, Transaction
from django.contrib.auth.models import User

def index(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    goals_count = FinancialGoal.objects.count()
    trans_count = Transaction.objects.count()
    
    context = {
        'goals_count': goals_count,
        'trans_count': trans_count,
    }
    return render(request, 'wallets/index.html', context)