from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Department, Program
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
import os
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as ex


def index(request):
    programs = [program for program in Program.objects.all()]
    files = [pd.read_excel(program.file) for program in programs]
    total_participants = sum([len(file.index) for file in files])
    years = set(program.year for program in programs)
    years = f'{min(years)}-{max(years)}'

    context = {
        'total_participants': total_participants,
        'years': years,
        'total_departments': Department.objects.count(),
        'total_programs': Program.objects.count(),
    }
    return render(request, 'main/index.html', context)


def departments(request):
    departments = Department.objects.order_by('name')

    context = {
        'departments': departments,
        'total_departments': Department.objects.count(),
        'num_departments': [x for x in range(departments.count())],
        'total_programs': Program.objects.count(),
    }
    print(context['num_departments'])
    return render(request, 'main/departments.html', context)


def department(request, slug):
    department = get_object_or_404(Department, slug=slug)
    # programs = Department.programs()
    programs = department.programs.all().order_by('-date_uploaded')
    context = {
        'programs': programs,
        'department': department,
        'total_departments': Department.objects.count(),
        'total_programs': Program.objects.count(),
    }
    return render(request, 'main/department.html', context)


def programs(request):
    programs = Program.objects.order_by('date_uploaded')

    context = {
        'programs': programs,
        'total_departments': Department.objects.count(),
        'total_programs': Program.objects.count(),
    }
    return render(request, 'main/programs.html', context)


def program_detail(request, id, slug):
    program = get_object_or_404(Program, id=id, slug=slug)
    file = pd.read_excel(program.file)
    csv = file.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"<a href='data:file/csv;base64,{b64}'download='{program.program}.csv' \
    class='btn btn-primary btn-xs float-right' target='_blank'><i class='la la-download'></i> Download File</a>"

    df = pd.DataFrame(file)
    gender = df['Gender'].value_counts()
    state = df['State'].value_counts()
    lga = df['L.G.A'].value_counts()

    # pie = go.Pie(values=gender, name='Test', labels=['Male', 'Female'], title='Gender')
    gender_pie = ex.pie(gender, values=gender, names=['Male', 'Female'])
    state_bar = ex.bar(state)
    lga_bar = ex.bar(lga)

    gender_plot = plot(gender_pie, output_type='div')
    state_plot = plot(state_bar, output_type='div')
    lga_plot = plot(lga_bar, output_type='div')

    context = {
        'program': program,
        'table': file.to_html(),
        'total_participants': len(df.index),
        'href': href,
        'total_departments': Department.objects.count(),
        'total_programs': Program.objects.count(),
        'gender_plot': gender_plot,
        'state_plot': state_plot,
        'lga_plot': lga_plot,
    }
    return render(request, 'main/program_detail.html', context)
