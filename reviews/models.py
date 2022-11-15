from django.db import models
# from .users import User


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
        # validators=[validate_year]
        verbose_name='Дата выхода произведения',
    )
    description = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Краткое содержание',
    )
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр произведения',
        related_name='genres',

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель для хранения постов."""

    text = models.TextField(
        verbose_name='Содержание',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        # User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Выберите автора',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )


class Comment(models.Model):
    """Модель для хранения комментариев к постам."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Добавьте комментарий',
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.title

class Follow(models.Model):
    """Модель для формирования подписки на авторов постов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор поста',
    )

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription')

