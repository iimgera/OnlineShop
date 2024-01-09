from django.db import models
from api.v1.models.catalog import Product
from api.v1.models.accounts import User


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товары'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено'
    )

    def __str__(self):
        return f'{self.user}  -  {self.product}'

    class Meta:
        app_label = 'cart'
        verbose_name='Корзина'
        verbose_name_plural = 'Корзины'
