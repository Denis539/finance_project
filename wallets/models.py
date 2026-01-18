from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    is_income = models.BooleanField(default=False, verbose_name="Это доход?")

    def __str__(self):
        prefix = "[+]" if self.is_income else "[-]"
        return f"{prefix} {self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name = "Категории"

class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="На что копим?")
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Нужная сумма")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Уже накоплено")
    deadline = models.DateField(verbose_name="Желаемая дата", null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.current_amount}/{self.target_amount})"

    class Meta:
        verbose_name = "Финансовая цель"
        verbose_name = "Финансовые цели"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    date = models.DateField(auto_now_add=True) 
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category.name}"

    class Meta:
        verbose_name = "Транзакция"
        verbose_name = "Транзакции"