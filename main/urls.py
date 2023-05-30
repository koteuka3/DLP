from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('lid-plans', views.plans, name = 'plans'),
]
