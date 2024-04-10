from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('program/<str:id>/<slug:slug>/', views.program_detail, name='program_detail'),
]
