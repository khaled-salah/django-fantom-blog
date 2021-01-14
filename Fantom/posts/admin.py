from django.contrib import admin
from .models import Post, Category, Tag, Comments


# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_filter = ['publishing_date']
    list_display = ['title', 'publishing_date']
    search_fields = ['content']

    class Meta:
        model = Post


class AdminComment(admin.ModelAdmin):
    list_filter = ['publishing_date']
    # list_display = ['name', 'publishing_date']
    search_fields = ['name', 'email', 'content', 'post__title']

    class Meta:
        model = Comments


admin.site.register(Post, AdminPost)
admin.site.register(Comments, AdminComment)
admin.site.register(Category)
admin.site.register(Tag)
