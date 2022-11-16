from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly
from reviews.models import Category, Genre, Title
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleUnSafeMethodsSerializer,
    TitleSafeMethodsSerializer,
)


class GenreViewSet(ListCreateDestroyViewSet):
    """Набор представлений для обработки экземпляров модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Набор представлений для обработки экземпляров модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Набор представлений для обработки экземпляров модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleUnSafeMethodsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return TitleUnSafeMethodsSerializer

        return TitleSafeMethodsSerializer
