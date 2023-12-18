from rest_framework import serializers
from api.v1.models.accounts import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'password_confirmation',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)

        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError('Укажите электронную почту для входа.')

        if not password:
            raise serializers.ValidationError('Укажите пароль.')

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Пользователь с такой электронной почтой не зарегистрирован")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль")

        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerificationSerializer(serializers.Serializer):
    otp_reset = serializers.CharField()


class CreateNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)

        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
