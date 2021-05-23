from django.contrib import admin
from django.db import models
from mdeditor.widgets import MDEditorWidget

from blog.models import Post, Category, Label


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'c_time', 'm_time', 'category', 'author', 'is_delete']
    fields = ['title', 'excerpt', 'body', 'category', 'labels', 'is_delete']
    list_editable = ['is_delete']
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Label)
