#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    :author: Si YingCheng
    :url: simple-syc.xyz
    :copyright: Copyright 2021-2021 siyingcheng@126.com ALL Rights Reserved
    :license: BSD
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('category/<int:pk>/', views.category, name='category'),
    path('label/<int:pk>/', views.label, name='label'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)