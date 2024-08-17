from django.contrib import admin
from olcha.models import Category, Group, Product, Image, Comment, Key, Value, Attribute


# Register your models here.
# admin.site.register(Category)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Group)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Image)


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['message','rating']

admin.site.register(Key)
admin.site.register(Value)
admin.site.register(Attribute)