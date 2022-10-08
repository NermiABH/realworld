from django.contrib import admin
from .models import CustomUser, Article, Comment
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Data for site', {'fields': ('email', 'password', 'username', 'image',
                                      'date_of_joining', 'sent_requests', 'favourites',
                                      'liked_articles', 'disliked_articles',
                                      'liked_comments', 'disliked_comments',)}),
        ('Personal data', {'fields': ('name', 'surname',
                                      'bio', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    readonly_fields = ('date_of_joining', )
    search_fields = ('email',)
    ordering = ('id',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',)
    readonly_fields = ('createdAt', 'updatedAt')
    ordering = ('id',)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Data for site', {'fields': ('parent',)}),)

#
admin.site.register(Comment)