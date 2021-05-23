import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from mdeditor.fields import MDTextField


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def posts(self):
        return self.post_set.filter(is_delete=False)


class Label(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=128)
    # body = models.TextField('正文')
    body = MDTextField('正文')
    c_time = models.DateField('创建时间', auto_now_add=True)
    m_time = models.DateField('修改时间', auto_now=True)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', null=True, blank=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField(Label, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', null=True, blank=True, on_delete=models.SET_NULL)
    is_delete = models.BooleanField('是否删除', default=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-c_time', '-pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        if not self.excerpt:
            _body = strip_tags(md.convert(self.body))
            length = min(len(_body), 197)
            self.excerpt = _body[:length] + '...'

        super().save(*args, **kwargs)
