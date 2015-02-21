# -*- coding: utf-8 -*-
from django.shortcuts import render

def index(request):
    context = {'hoga': 'fuga'}
    return render(request, 'analysis/index.html', context)

