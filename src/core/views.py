
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'core/index.html')

