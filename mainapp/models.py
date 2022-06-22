from django.db import models


class ProductTable(models.Model):
    """ Таблица, хранящая информацию по заказам """
    record_number = models.PositiveIntegerField('№')
    order_number = models.PositiveIntegerField('заказ №')
    cost_dollars = models.PositiveIntegerField('стоимость,$')
    cost_rubles = models.PositiveIntegerField('стоимость в руб.')
    delivery_time = models.DateField('срок поставки')


class CurrenciesRates(models.Model):
    """ Таблица с курсами валют """
    currency_name = models.CharField('Тикер валюты', max_length=10)
    rate = models.FloatField('Значение относительно рубля')
