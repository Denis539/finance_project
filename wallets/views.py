from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>SmartSave MVP</h1><p>Система интеллектуального планирования накоплений запущена!</p>")
