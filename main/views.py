from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Work
from .forms import WorkForm
from django.contrib import messages
from django import forms
import requests
from .utils import generate_event_list
import datetime
import json
from .weather import check_weather_conditions

def index(request):
    return render(request, 'main/index.html')

def plans(request):
    if request.method == 'GET':
       form = WorkForm()
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            work_name = form.cleaned_data['work_name'],
            work_date = form.cleaned_data['work_date'],
            work_time1 = form.cleaned_data['work_time1'],
            work_time2 = form.cleaned_data['work_time2']
            form.save()
            # veiksmīgi reģistrēts darbs
            messages.success(request, "Darbs veiksmīgi reģistrēts!")
            return redirect('plans')
    else:
        form = WorkForm()

    favorable_conditions = check_weather_conditions()
    missions = generate_event_list()

    context = {
        'form': form,
        'favorable_conditions': favorable_conditions,
        'missions': missions,
    }
    return render(request, 'main/plans.html', context=context)














