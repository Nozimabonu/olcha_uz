from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from olcha.models import Category, Group, Product


class CategoryModelSerializer(ModelSerializer):
    image = serializers.ImageField(max_length=None)
    group_count = serializers.SerializerMethodField()

    def get_group_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image', 'group_count']


class GroupModelSerializer(ModelSerializer):
    # category = CategoryModelSerializer(read_only=True)
    category_slug = serializers.SlugField(source='category.slug')
    category_title = serializers.CharField(source='category.title')
    full_image_url = serializers.SerializerMethodField(method_name='foo')
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, instance):
        products = Product.objects.annotate(order_count=Count('order'))
        return instance.products.count()

    def foo(self, obj):
        image_url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Group
        exclude = ('image',)


class ProductModelSerializer(ModelSerializer):
    category_name = serializers.CharField(source='group.category.title')
    group_name = serializers.CharField(source='group.title')
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_info = serializers.SerializerMethodField()

    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attrs = instance.attributes.all().values('key__name', 'value__name')
        # attrs = instance.attributes.all()
        # my_list = [{attr.key.name: attr.value.name} for attr in attrs]
        # print(my_list)

        product_attributes = [
            {
                attribute['key__name']: attribute['value__name']
            }
            for attribute in attrs
        ]
        return product_attributes

    def get_comment_info(self, obj):
        # comments = [
        #     {
        #         'message': comment.message,
        #         'rating': comment.rating,
        #         'username': comment.user.username
        #     }
        #     for comment in obj.comments.all()]
        # return comments

        return obj.comments.all().values('message', 'rating', 'user__username')

    def get_all_images(self, instance):
        request = self.context.get('request', None)
        images = instance.images.all().order_by('-is_primary', '-id')
        all_images = []
        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))

        return all_images

    def get_avg_rating(self, product):
        avg_rating = product.comments.all().aggregate(avg=Round(Avg('rating')))
        print(avg_rating)
        return avg_rating.get('avg')
        # avg_rating = {'avg':value}

    def get_image(self, obj):
        # image = Image.objects.filter(is_primary=True, product=obj.first()
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # if user in Product.objects.filter(is_liked=user.id):
            if user in obj.is_liked.all():
                return True
            return False

    class Meta:
        model = Product
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=255, required=True)


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=125, required=False)
    last_name = serializers.CharField(max_length=125, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def validate_username(self, username):

        if User.objects.filter(username=username).exists():
            detail = {
                "data": f"This {username} already exists"
            }
            raise serializers.ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            data = {
                'error': 'Passwords do not match'
            }
            raise serializers.ValidationError(detail=data)

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop('password')
        passowrd2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(passowrd)
        # user.save()
        Token.objects.create(user=user)
        return user
