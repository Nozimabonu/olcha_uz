from django.contrib import admin
from django.contrib.auth.models import User, Group

from olcha import models

# Register your models here.


admin.site.unregister(models.User)
admin.site.register(models.Image)
admin.site.register(models.Comment)
admin.site.register(models.Key)
admin.site.register(models.Value)
admin.site.register(models.Attribute)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'slug']
    prepopulated_fields = {'slug': ('group_name',)}


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug']
    prepopulated_fields = {'slug': ('product_name',)}
