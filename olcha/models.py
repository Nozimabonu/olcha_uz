from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, blank=True)
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)

            super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'categories'


class Group(BaseModel):
    group_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.group_name)

        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'groups'


class Product(BaseModel):
    product_name = models.CharField(max_length=100, null=False, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    # quantity = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    users_like = models.ManyToManyField(User, related_name='likes', blank=True, db_table='users_like')

    @property
    def discount_price(self):
        if self.discount > 0:
            return self.price * (self.discount / 100)

        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'products'


class Image(models.Model):
    image_name = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_images', null=True, blank=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_images', null=True,
    #                              blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'images'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value, null=True, blank=True)
    message = models.TextField()
    file = models.FileField(upload_to='comments/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

    class Meta:
        db_table = 'comments'


class AttributeKey(models.Model):
    attribute_key = models.CharField(max_length=100)

    def __str__(self):
        return self.attribute_key


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)

    def __str__(self):
        return self.attribute_value


class AttributeProduct(models.Model):
    key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

