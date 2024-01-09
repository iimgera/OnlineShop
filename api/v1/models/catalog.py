from django.db import models
from api.v1.models.accounts import User


class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='Название',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'catalog'
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(
        max_length=100, verbose_name='Название товара'
    )
    photo = models.ImageField(
        upload_to='catalog/photos/',
        verbose_name='Фотография товара'
    )
    description = models.TextField(
        verbose_name='Описание товара'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена'
    )
    available = models.BooleanField(
        default=True, verbose_name='Наличие'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        verbose_name='Категория', related_name='products'
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'catalog'
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
