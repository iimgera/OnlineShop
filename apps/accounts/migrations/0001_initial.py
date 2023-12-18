# Generated by Django 5.0 on 2023-12-17 20:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, default='Еще не заполнен', max_length=60, null=True, unique=True, verbose_name='Почта')),
                ('username', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('full_name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True, unique=True, verbose_name='Номер телефона')),
                ('otp_reset', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_reset_created_at', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(related_name='custom_user', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='custom_user', to='auth.permission')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
