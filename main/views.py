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
from collections import Counter


def index(request):
    programs = [program for program in Program.objects.all()]
    dfs = [pd.read_excel(program.file) for program in programs]
    # data_frame_new = dfs[0][['Name of the Beneficiary ', 'Gender', 'Age Range', 'Phone number ', 'Email Adress',
    #                          'Capacity Building Program', 'State', 'L.G.A', 'Year ', 'Department', 'Duration',
    #                          'Skills/experience level',
    #                          'Training category (Digital literacy, Digital skills or IT specialised skills', 'Status']]

    num_pro_by_dept = [program.department.name for program in programs]
    temp_count = Counter(num_pro_by_dept)
    # count = [[i, temp_count[i]] for i in temp_count]
    debt_df = pd.DataFrame(num_pro_by_dept, columns=['Department'])
    department = debt_df['Department'].value_counts()
    dept_bar = ex.bar(department, color=department.index.tolist())
    dept_plot = plot(dept_bar, output_type='div')

    years = [program.year for program in programs]
    temp_count = Counter(years)
    year_df = pd.DataFrame(years, columns=['Year'])
    year = year_df['Year'].value_counts().sort_index()
    # x=year.index.tolist(), y=year.values.tolist()
    year_line = ex.line(year, markers=True)\
        .update_layout(xaxis_title='Year', yaxis_title='Number of Programs').update_traces(line_color='red')
    year_plot = plot(year_line, output_type='div')

    df = pd.concat(dfs, ignore_index=True)
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"<a href='data:file/csv;base64,{b64}'download='data.csv' \
        class='btn btn-primary btn-xs float-right' target='_blank'><i class='la la-download'></i> Download File</a>"
    gender = df['Gender'].value_counts()
    state = df['State'].value_counts()
    lga = df['L.G.A'].value_counts()
    age = df['Age Range'].value_counts()

    age_bar = ex.bar(age, opacity=1, color=age.index.tolist())
    age_plot = plot(age_bar, output_type='div')

    gender_pie = ex.pie(gender, values=gender,
                        names=gender.index.tolist()
                        )
    gender_plot = plot(gender_pie, output_type='div', include_plotlyjs=True, show_link=False)

    state_bar = ex.bar(state, opacity=1, height=900, orientation='h')
    state_plot = plot(state_bar, output_type='div',
                      # show_link=False, link_text='',
                      # image_filename=f'{program.program}', image='jpeg'
                      )

    lga_bar = ex.bar(lga, opacity=1, height=700, orientation='h')
    lga_plot = plot(lga_bar, output_type='div')

    total_participants = sum([len(df.index) for df in dfs])
    years = set(program.year for program in programs)
    total_years = len(years)
    years = f'{min(years)}-{max(years)}'

    context = {
        'total_participants': total_participants,
        'total_years': total_years,
        'years': years,
        'total_departments': Department.objects.count(),
        'total_programs': Program.objects.count(),
        'href': href,
        'gender_plot': gender_plot,
        'state_plot': state_plot,
        'lga_plot': lga_plot,
        'table': df.to_html(),
        'dept_plot': dept_plot,
        'age_plot': age_plot,
        'year_plot': year_plot,
    }
    return render(request, 'main/index.html', context)


def departments(request):
    departments = Department.objects.order_by('name')

    dept = [dept.name for dept in departments]
    num_pro = [dept.programs.count() for dept in departments]
    df = pd.DataFrame(dict(
        department=dept,
        value=num_pro))
    depts_bar = ex.bar(df, x='department', y='value', opacity=1, color='department')
    depts_plot = plot(depts_bar, output_type='div')

    context = {
        'departments': departments,
        'total_departments': Department.objects.count(),
        'num_departments': [x for x in range(departments.count())],
        'total_programs': Program.objects.count(),
        'depts_plot': depts_plot,
    }
    return render(request, 'main/departments.html', context)


def department(request, slug):
    department = get_object_or_404(Department, slug=slug)
    # programs = Department.programs()
    programs = department.programs.all().order_by('-date_uploaded')

    years = [program.year for program in programs]
    temp_count = Counter(years)
    year_df = pd.DataFrame(years, columns=['Year'])
    year = year_df['Year'].value_counts().sort_index()
    year_line = ex.line(year, markers=True) \
        .update_layout(xaxis_title='Year', yaxis_title='Number of Programs').update_traces(line_color='blue')
    year_plot = plot(year_line, output_type='div')

    context = {
        'programs': programs,
        'department': department,
        'total_departments': Department.objects.count(),
        'total_programs': Program.objects.count(),
        'year_plot': year_plot,
    }
    return render(request, 'main/department.html', context)


def programs(request):
    programs = Program.objects.order_by('-date_uploaded')

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
    gender_pie = ex.pie(gender, values=gender,
                        names=gender.index.tolist()
                        )
    state_bar = ex.bar(state, opacity=1, height=900, orientation='h')
    lga_bar = ex.bar(lga, opacity=1, height=700, orientation='h')

    gender_plot = plot(gender_pie, output_type='div', include_plotlyjs=True, show_link=False)
    state_plot = plot(state_bar, output_type='div',
                      # show_link=False, link_text='',
                      # image_filename=f'{program.program}', image='jpeg'
                      )
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
