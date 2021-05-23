import re

import markdown
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension, slugify

from blog.models import Post, Category, Label


def index(request):
    posts = Post.objects.filter(is_delete=False).order_by('-c_time', '-pk')
    return render(request, 'blog/index.html', context={'title': '文章列表', 'posts': posts})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.is_delete:
        raise Http404('No %s matches the given query.' % post.title)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'title': post.title, 'post': post})


def archive(request, year, month):
    posts = Post.objects.filter(is_delete=False,
                                c_time__year=year,
                                c_time__month=month).order_by('-c_time', '-pk')
    return render(request, 'blog/index.html', context={'title': f'归档 - {year} 年 {month} 月', 'posts': posts})


def category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(is_delete=False,
                                category=cat).order_by('-c_time', '-pk')
    return render(request, 'blog/index.html', context={'title': '分类 - ' + cat.name, 'posts': posts})


def label(request, pk):
    lab = get_object_or_404(Label, pk=pk)
    posts = Post.objects.filter(is_delete=False,
                                labels=lab).order_by('-c_time', '-pk')
    return render(request, 'blog/index.html', context={'title': '标签 - ' + lab.name, 'posts': posts})
