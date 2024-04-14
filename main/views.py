from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Department, Program
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os


def index(request):
    return render(request, 'main/index.html')


def departments(request):
    departments = Department.objects.order_by('name')

    context = {
        'departments': departments,
        'total_departments': Department.objects.count(),
        'num_departments': [x for x in range(departments.count())],
    }
    return render(request, 'main/departments.html', context)


def department(request, slug):
    department = get_object_or_404(Department, slug=slug)
    # programs = Department.programs()
    print(department.programs.all())
    context = {
        # 'programs': programs,
        'department': department
    }
    return render(request, 'main/department.html', context)


def programs(request):
    programs = Program.objects.order_by('date_uploaded')

    context = {
        'programs': programs,
    }
    return render(request, 'main/programs.html', context)


def program_detail(request, id, slug):
    program = get_object_or_404(Program, id=id, slug=slug)
    file = pd.read_excel(program.file)
    csv = file.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"<a href='data:file/csv;base64,{b64}'download='{program.program}.csv' target='_blank'>Download File</a>"

    df = pd.DataFrame(file)
    # gender = df['Gender'].value_counts()
    # print(df['State'].value_counts())

    context = {
        'program': program,
        'table': file.to_html(),
        'total_participants': len(df.index),
        'href': href,
        'total_departments': Department.objects.count(),
    }
    return render(request, 'main/program_detail.html', context)