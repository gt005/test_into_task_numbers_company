from django.db import models


class ProductTable(models.Model):
    ''' Таблица, хранящая информацию по заказам '''
    record_number = models.PositiveIntegerField("№")
    order_number = models.PositiveIntegerField("заказ №")
    cost_dollars = models.PositiveIntegerField("стоимость,$")
    cost_rubles = models.PositiveIntegerField("стоимость в руб.")
    delivery_time = models.DateField("срок поставки")


class ProductCurrencyWorker(ProductTable):
    ''' Класс для пересчета стоимости по курсу ЦБ '''
    usdrub_exchange_rate = 53.264  # Последний сохраненный курс пары доллар/рубль

    class Meta:
        proxy = True
