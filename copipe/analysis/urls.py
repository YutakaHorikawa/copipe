# -*- coding: utf-8 -*-
# polls/urls.py
from django.conf.urls import patterns, url
from analysis import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='analysis_index'),
    url(r'analyze/$', views.analyze, name='analysis_analyze'),
)
