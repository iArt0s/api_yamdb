from rest_framework import serializers
from users.models import User
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class GenreSerializer(serializers.ModelSerializer):
    """(Де-)Сериализатор для модели Genre приложения reviews."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """(Де-)Сериализатор для модели Category приложения reviews."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleUnSafeMethodsSerializer(serializers.ModelSerializer):
    """Стандартный (де-)сериализатор для модели Title приложения reviews."""
    genre = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSafeMethodsSerializer(serializers.ModelSerializer):
    """
    (Де-)Сериализатор для модели Title приложения reviews,
    использующий вложенные сериализаторы.
    Цель использоваия - получение  вместе с объектом Title
    списка, состоящего из привязанных к нему объектов Genre и Category
    вместо ссылок на данные объекты.
    """
    
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SelfUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
