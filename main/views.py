from django.shortcuts import render, get_object_or_404
from .models import Department, Program
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os


def index(request):
    programs = Program.objects.all()

    context = {
        'programs': programs,
    }

    return render(request, 'main/index.html', context)


def program_detail(request, id, slug):
    program = get_object_or_404(Program, id=id, slug=slug)
    file = pd.read_excel(program.file)
    csv = file.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"<a href='data:file/csv;base64,{b64}'download='{program.program}.csv' target='_blank'>Download File</a>"

    df = pd.DataFrame(file)
    gender = df['Gender'].value_counts()
    print(df['State'].value_counts())
    # fig, ax = plt.subplots()
    # bar = df['Gender'].value_counts().plot.bar()
    # img = fig.savefig('sample.png')
    # image = f"<img src='{img}'>"

    context = {
        'program': program,
        'table': file.to_html(),
        'href': href,
        # 'image': image,
        'male': gender['M']
    }
    return render(request, 'main/program_detail.html', context)
