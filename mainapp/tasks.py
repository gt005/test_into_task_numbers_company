from .models import *

from typing import Tuple
from datetime import datetime

from celery import shared_task
from mainapp.addons_python.google_table_exporter import GoogleTableExporter
from mainapp.addons_python.currency_exporter import usdrub_currency_export


@shared_task(bind=True)
def update_table_in_interval(self) -> None:
    """ Получает актуальные данные из таблицы google и проверяет их на актуальность """

    data_rows_from_sheet: Tuple[Tuple[int, int, int, datetime], ...] = GoogleTableExporter().get_values()
    hashed_data = hash(data_rows_from_sheet)

    current_rate = CurrenciesRates.objects.filter(currency_name='USD')
    if not current_rate:  # Валюта не была найдена в таблице курсов валют
        print('log: Данной валюты не существует, данные таблицы НЕ обновлены')
        return
    current_rate = current_rate[0].rate

    product_table_hash_object = ProductTableHash.objects.all()
    if not product_table_hash_object:  # Хеш еще не был рассчитан ни разу (первый запуск программы)
        product_table_hash_object = ProductTableHash()
        product_table_hash_object.save()
    else:
        product_table_hash_object = product_table_hash_object[0]

    if product_table_hash_object.table_hash == hashed_data:  # Если хеш совпадает с прошлым, то запись не изменялась
        return

    # Хеш различается или не существует => меняем таблицу
    product_table_hash_object.table_hash = hashed_data
    product_table_hash_object.save()
    ProductTable.objects.all().delete()
    for row in data_rows_from_sheet:
        ProductTable(
            record_number=row[0],
            order_number=row[1],
            cost_dollars=row[2],
            cost_rubles=(row[2] * current_rate),
            delivery_time=row[3],
        ).save()


@shared_task(bind=True)
def update_currency_rate(self, currency_name: str) -> None:
    """ Данные из парсера сохраняет в таблицу последних значений валют  """
    current_currency_rate = usdrub_currency_export(currency_name)  # Получение курса цб по API цбрф
    row_with_needed_currency = CurrenciesRates.objects.filter(currency_name='USD')  # Поиск существуещего значения
    if not row_with_needed_currency:
        CurrenciesRates(
            currency_name='USD',
            rate=current_currency_rate
        ).save()
    elif row_with_needed_currency[0].rate != current_currency_rate:
        update_currency_in_table(current_currency_rate)  # Пересчитываем по новому курсу стоимость всех продуктов
        row_with_needed_currency[0].rate = current_currency_rate
        row_with_needed_currency[0].save()


def update_currency_in_table(new_rate: float) -> None:
    """ Функция пересчитывает колонну со стоимостью в рублях по курсу new_rate """
    for product in ProductTable.objects.all():
        product.cost_rubles = product.cost_dollars * new_rate
        product.save()
