from django.db import models
from api.auth.auth import User
from api.v1.models.catalog import Product


class OrderStatusChoices(models.TextChoices):
    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN_PROGRESS", "В процессе"
    DONE = "DONE", "Закрыт"


class Order(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name='Товары'
    )
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
        verbose_name='Статус заказа'
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, verbose_name='Общая цена'
    )
    total_items = models.PositiveSmallIntegerField(
        default=0, verbose_name='Всего'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Изменено'
    )

    def __str__(self):
        return f'{self.creator}  {self.status}'

    class Meta:
        app_label = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        self.total_price = sum(item.get_cost() for item in self.positions.all())
        self.total_items = sum(item.quantity for item in self.positions.all())
        super(Order, self).save(*args, **kwargs)


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Количество'
    )

    def get_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.creator}  {self.status}'

    class Meta:
        app_label = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'