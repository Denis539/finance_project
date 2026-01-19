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
    # Обработка форм
    if request.method == 'POST':
        if 'add_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
        elif 'add_category' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
        elif 'add_goal' in request.POST:
            form = FinancialGoalForm(request.POST)
            if form.is_valid() and FinancialGoal.objects.filter(user=request.user).count() < 3:
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
        return redirect('index')

    # Расчеты
    user_transactions = Transaction.objects.filter(user=request.user)
    incomes = user_transactions.filter(category__is_income=True).aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = user_transactions.filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum'] or 0
    total_saved = float(incomes - expenses)
    
    # Темп накопления
    first_t = user_transactions.order_by('date').first()
    daily_pace = 0.0
    if first_t and first_t.date:
        try:
            f_date = first_t.date.date() 
        except AttributeError:
            f_date = first_t.date      
        days_active = (date.today() - f_date).days
        if total_saved > 0:
            daily_pace = float(total_saved) / max(days_active, 1)

    # Цели и прогнозы
    goals = FinancialGoal.objects.filter(user=request.user)
    g_count = goals.count()
    for g in goals:
        target = float(g.target_amount)
        allocated = min(max(total_saved / g_count, 0), target) if g_count > 0 else 0
        g.current_allocated = round(allocated, 2)
        g.real_percent = int((allocated / target) * 100) if target > 0 else 0
        needed = target - allocated
        pace_share = (daily_pace / g_count) if g_count > 0 else 0
        if needed <= 0:
            g.forecast = "Достигнуто!"
        elif pace_share > 0:
            days_left = int(needed / pace_share)
            g.forecast = f"Будет накоплено через {days_left} дн."
        else:
            g.forecast = "Нужны доходы для прогноза"

    return render(request, 'wallets/index.html', {
        'form': TransactionForm(),
        'category_form': CategoryForm(),
        'goal_form': FinancialGoalForm(),
        'goals': goals,
        'total_saved': round(total_saved, 2),
        'daily_pace': round(daily_pace, 2),
        'latest_transactions': user_transactions.order_by('-id')[:5],
        'chart': generate_pie_chart(float(incomes), float(expenses)),
    })

# Функция регистрации нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'registration/register.html', {'form': UserCreationForm()})

# Функция безопасного удаления цели
@login_required
def delete_goal(request, goal_id):
    goal = FinancialGoal.objects.filter(user=request.user, id=goal_id).first()
    if goal:
        goal.delete()
    return redirect('index')