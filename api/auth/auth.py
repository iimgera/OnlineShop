from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.v1.models.accounts import User
from .utils import generate_otp
from api.v1.serializers.accounts import (
    RegistrationSerializer, LoginSerializer,
    PasswordResetRequestSerializer,
    OTPVerificationSerializer,
    CreateNewPasswordSerializer,
)


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                raise ValidationError({'email': ['Пользователь с таким email уже существует.']})

            user = serializer.save()
            send_mail(
                'Online-shop',
                'Вы успешно зарегистрировались!',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({
                'status': 200,
                'message': 'Регистрация успешна. Проверьте электронную почту для подтверждения.',
            })
        except ValidationError as e:
            return Response({
                'status': 400,
                'message': 'Проверьте корректность заполнения параметров',
                'data': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if 'email' not in request.data:
            return Response({
                'status': 400,
                'message': 'Укажите электронную почту для входа.',
            }, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=request.data['email'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Отсутствует refresh_token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'Вы успешно вышли из системы'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Ошибка при выходе из системы: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetRequestView(APIView):
    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response(
                {'error': 'Для этого пользователя не найден подтвержденный адрес электронной почты'},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp = generate_otp()
        user.otp_reset = otp
        user.save()

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения : {otp}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Код подтверждения отправлен успешно'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def put(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response(
                {'error': 'Неверный код подтверждения или пользователь не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_otp = generate_otp()
        user.otp_reset = new_otp
        user.save()

        send_mail(
            'Код подтверждения',
            f'Ваш новый код подтверждения : {new_otp}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Код подтверждения успешно обновлен'}, status=status.HTTP_200_OK)


class OTPVerificationView(APIView):
    @swagger_auto_schema(request_body=OTPVerificationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp_reset']

        try:
            user = User.objects.get(otp_reset=otp)
        except User.DoesNotExist:
            return Response({'error': 'Недействительный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)

        if user.otp_expired():
            return Response({'error': 'Срок действия кода подтверждения истек'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Код подтверждения успешно подтвержден'}, status=status.HTTP_200_OK)


class CreateNewPasswordView(APIView):
    @swagger_auto_schema(
        request_body=CreateNewPasswordSerializer,
        manual_parameters=[
            openapi.Parameter(
                'email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='email для сброса пароля',
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        email = self.request.query_params.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Недействительный email'}, status=status.HTTP_400_BAD_REQUEST)

        if user.otp_expired():
            return Response({'error': 'Срок действия код подтверждения истек'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.otp_reset = None
        user.otp_reset_created_at = None
        user.save()

        return Response({'message': 'Пароль установлен успешно'}, status=status.HTTP_200_OK)
