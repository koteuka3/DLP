from .models import Work
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django import forms
import datetime as dt
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.utils import timezone
from django.forms import TimeInput, TimeField
from django.utils.translation import gettext_lazy as _


def get_min_date():
    return datetime.date.today() + datetime.timedelta(weeks=0)


class WorkForm(ModelForm):
    work_name = forms.CharField(label='Darba nosaukums',
                                widget=forms.TextInput(attrs={
                                "class": "form-control mb-3",
                                "placeholder": "Ievadiet darba nosaukumu",
                                "maxlength": "20",
    }))
    work_date = forms.DateField(label='Darba diena',
                                validators=[MinValueValidator(get_min_date)],
                                widget=forms.DateInput(attrs={
                                "type": "date",
                                'min': get_min_date,
                                "class": "form-control mb-3",
    }))
    work_time1 = forms.TimeField(label='Sākums',
                                 widget=forms.TimeInput(attrs={
                                 "type": "time",
                                 "class": "form-control mb-3",
    }))
    work_time2 = forms.TimeField(label='Beigas',
                                 widget=forms.TimeInput(attrs={
                                 "type": "time",
                                 "class": "form-control mb-3",
    }))
    class Meta:
        model = Work
        fields = ["work_name", "work_date", "work_time1", "work_time2"]



