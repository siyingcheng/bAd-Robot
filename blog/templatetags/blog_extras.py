#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    :author: Si YingCheng
    :url: simple-syc.xyz
    :copyright: Copyright 2021-2021 siyingcheng@126.com ALL Rights Reserved
    :license: BSD
"""
from django import template

from blog.models import Post, Category, Label

register = template.Library()


@register.inclusion_tag('blog/include/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.filter(is_delete=False).order_by('-c_time', '-pk')[:num]
    }


@register.inclusion_tag('blog/include/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('c_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/include/_categories.html', takes_context=True)
def show_categories(context):
    return {'category_list': Category.objects.all()}


@register.inclusion_tag('blog/include/_labels.html', takes_context=True)
def show_labels(context):
    return {'label_list': Label.objects.all()}
