from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    """(Де-)Сериализатор для модели Genre приложения reviews."""

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """(Де-)Сериализатор для модели Category приложения reviews."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


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
