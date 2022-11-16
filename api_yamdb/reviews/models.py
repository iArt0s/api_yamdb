from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Genre(models.Model):
    """Модель для сортировки произведений по жанрам."""

    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор жанра',
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для сортировки произведений по категориям."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор категории',
    )


class Title(models.Model):
    """Модель для объявления произведений."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Дата выхода произведения',
    )

    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Краткое содержание',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        null=True,
        related_name='genres',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория произведения',
    )
    rating = models.IntegerField(
        null=True,
        verbose_name='Рейтинг произведения',
    )

    def validate_year(value):
        """Метод, позволяющий отследить корректный год выпуска произведения."""
        if value > timezone.now().year:
            raise ValidationError(
                {'year': ('Год выпуска не может быть в будущем!')}
            )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
