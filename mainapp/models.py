from django.db import models


class ProductTable(models.Model):
    """ Таблица, хранящая информацию по заказам """
    record_number = models.PositiveIntegerField('№')
    order_number = models.PositiveIntegerField('заказ №')
    cost_dollars = models.PositiveIntegerField('стоимость,$')
    cost_rubles = models.PositiveIntegerField('стоимость в руб.')
    delivery_time = models.DateField('срок поставки')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Заказ №{self.order_number} Поставка {self.delivery_time}'


class ProductTableHash(models.Model):
    """ Хранит значение хеша таблицы ProductTable """
    _table_hash = models.CharField('Хеш таблицы ProductTable', max_length=50, default='0')
    # Значение будет посчитано при первом парсинге таблицы

    @property
    def table_hash(self):
        return int(self._table_hash)

    @table_hash.setter
    def table_hash(self, value):
        self._table_hash = str(value)

    class Meta:
        verbose_name = 'Значение хеша таблицы'
        verbose_name_plural = 'Значения хеша таблицы'


class CurrenciesRates(models.Model):
    """ Таблица с курсами валют
        :currency_name Тикер нужной валюты заглавными латинскими буквами (пример USD)"""
    currency_name = models.CharField('Тикер валюты', max_length=10)
    rate = models.FloatField('Значение относительно рубля')

    def __str__(self):
        return f'{self.currency_name}: {self.rate} руб.'

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'
