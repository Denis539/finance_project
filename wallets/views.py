from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from .models import FinancialGoal, Transaction, Category
from .forms import TransactionForm, CategoryForm, FinancialGoalForm
from .utils import generate_pie_chart
from datetime import date, timedelta

@login_required
def index(request):
    transaction_form = TransactionForm()
    category_form = CategoryForm()
    goal_form = FinancialGoalForm()
    goal_error = None

    if request.method == 'POST':
        if 'add_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect('index')
        
        elif 'add_category' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')

        elif 'add_goal' in request.POST:
            if FinancialGoal.objects.filter(user=request.user).count() >= 3:
                goal_error = "Лимит: 3 цели. Сосредоточьтесь на главном!"
                goal_form = FinancialGoalForm(request.POST)
            else:
                form = FinancialGoalForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return redirect('index')

    user_transactions = Transaction.objects.filter(user=request.user)
    
    incomes = user_transactions.filter(category__is_income=True).aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = user_transactions.filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum'] or 0
    total_saved = incomes - expenses
    
    first_transaction = user_transactions.order_by('date').first()
    daily_pace = 0
    if first_transaction:
        raw_date = first_transaction.date if first_transaction.date else date.today()
        try:
            f_date = raw_date.date()
        except AttributeError:
            f_date = raw_date
            
        days_active = (date.today() - f_date).days
        days_active = max(days_active, 1) 
        daily_pace = float(total_saved) / days_active

    goals = FinancialGoal.objects.filter(user=request.user)
    goals_count = goals.count()

    for goal in goals:
        target = float(goal.target_amount)
        current_total = float(total_saved)
        current_pace = float(daily_pace)

        share_of_balance = current_total / goals_count if goals_count > 0 else 0
        share_of_pace = current_pace / goals_count if goals_count > 0 else 0

        allocated = min(max(share_of_balance, 0), target)
        goal.current_allocated = round(allocated, 2)
        
        goal.real_percent = int((allocated / target) * 100) if target > 0 else 0
        amount_needed = target - allocated

        if amount_needed <= 0:
            goal.forecast = "Цель достигнута! 🎉"
        elif share_of_pace > 0:
            days_left = amount_needed / share_of_pace
            forecast_date = date.today() + timedelta(days=int(days_left))
            goal.forecast = f"При делении бюджета на {goals_count} ч., накопите к {forecast_date.strftime('%d.%m.%Y')}"
        else:
            goal.forecast = "Нужен стабильный доход для прогноза."

    chart = generate_pie_chart(incomes, expenses)

    context = {
        'form': transaction_form,
        'category_form': category_form,
        'goal_form': goal_form,
        'goal_error': goal_error,
        'goals': goals,
        'total_saved': round(total_saved, 2),
        'latest_transactions': user_transactions.order_by('-id')[:5],
        'chart': chart,
        'incomes': incomes,
        'expenses': expenses,
        'daily_pace': round(daily_pace, 2),
    }
    
    return render(request, 'wallets/index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})