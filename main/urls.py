from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('departments/', views.departments, name='departments'),
    path('departments/<slug:slug>/', views.department, name='department'),
    path('programs/', views.programs, name='programs'),
    path('programs/<str:id>/<slug:slug>/', views.program_detail, name='program_detail'),
]
