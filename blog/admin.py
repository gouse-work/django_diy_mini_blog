from django.contrib import admin
from .models import Blog,BlogAuthor,BlogComment

#admin.site.register(Blog)
#admin.site.register(BlogAuthor)
#admin.site.register(BlogComment)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('get_short_title', 'get_short_description', 'author', 'post_date')
    fieldsets = [
        ('Info', {
            'fields': ('name', 'description', 'author', 'post_date')
        })
    ]
    list_filter = ('post_date', 'author')

class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0


@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    inlines = [BlogInline]

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    pass