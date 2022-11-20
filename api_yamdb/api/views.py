from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, generics, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsOnlyAdmin, IsReviewAndComment
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    RegisterSerializer,
    VerifySerializer,
    UserSerializer,
    SelfUserSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from api_yamdb.settings import EMAIL_ADMIN
from users.models import User


class GenreViewSet(ListCreateDestroyViewSet):
    """Набор представлений для обработки экземпляров модели Genre."""
    queryset = Genre.objects.all()
    lookup_field = ('slug')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Набор представлений для обработки экземпляров модели Category."""
    queryset = Category.objects.all()
    lookup_field = ('slug')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Набор представлений для обработки экземпляров модели Title."""
    serializer_class = TitlePostSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return TitlePostSerializer

        return TitleGetSerializer

    def get_queryset(self):
        if self.action in ('retrieve', 'list'):
            return Title.objects.prefetch_related(
                'reviews').all().annotate(rating=Avg('reviews__score'))

        return Title.objects.all()


class RegisterView(viewsets.ModelViewSet):
    """Набор представлений для обработки регистрации пользователей."""
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        send_mail(
            subject=f'Привет {user.username} ! Код для получения токена.',
            message=f'Код: {token}',
            from_email=EMAIL_ADMIN,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyUserView(generics.GenericAPIView):
    """Обработчик для проверки аутентификации пользователей."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifySerializer

    def post(self, serializer):
        verify_code = serializer.data.get('confirmation_code')
        if serializer.data == {}:
            return Response({'error': 'Запрос без параметров'},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'username' not in serializer.data:
            return Response({'error': 'Запрос без username'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User, username=serializer.data.get('username'))
        if not default_token_generator.check_token(user, verify_code):
            return Response({'error': 'Код подтверждения неверный!'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({'access': str(refresh.access_token)},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Набор представлений для обработки экземпляров модели User."""
    queryset = User.objects.all()
    permission_classes = (IsOnlyAdmin,)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    lookup_field = ('username')
    search_fields = ('=username',)

    def get_permissions(self):
        if self.kwargs.get('username') == 'me':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def partial_update(self, request, username):
        if 'me' == username:
            serializer = SelfUserSerializer(
                self.request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, username):
        user = self.request.user
        if 'me' != username:
            user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, username):
        if 'me' == username:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = User.objects.get(username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    """Набор представлений для обработки экземпляров модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsReviewAndComment, permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get('title_id')
        get_object_or_404(Title, pk=pk)
        return Review.objects.filter(title__pk=pk)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Набор представлений для обработки экземпляров модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsReviewAndComment, permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get('review_id')
        get_object_or_404(Review, pk=pk)
        return Comment.objects.filter(review__pk=pk)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
