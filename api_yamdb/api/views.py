from rest_framework import viewsets, status, permissions, generics
from .serializers import RegisterSerializer, VerifySerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator


class RegisterView(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_mail = User.objects.get(email=user_data['email'])
        user_name = User.objects.get(username=user_data['username'])
        token = default_token_generator.make_token(user_name)
        send_mail(
            subject=f'Привет {user_name}!.Код для получения токена.',
            message=f'Код: {token}',
            from_email='admin@gmail.com',
            recipient_list=[user_mail.email],
            fail_silently=False,
        )


class VerifyUserView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifySerializer

    def post(self, serializer):
        verify_code = serializer.data.get('confirmation_code')
        user= User.objects.get(username=serializer.data.get('username'))
        if not default_token_generator.check_token(user, verify_code): 
            return Response({'error': f'Код подтверждения неверный!'}, status=status.HTTP_400_BAD_REQUEST) 
        user.is_active=True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
