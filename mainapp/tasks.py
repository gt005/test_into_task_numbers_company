from .models import CurrenciesRates

from celery import shared_task
from mainapp.addons_python.google_table_exporter import GoogleTableExporter
from mainapp.addons_python.currency_exporter import usdrub_currency_export


@shared_task(bind=True)
def update_table_in_interval(self):
    """  """

    a = GoogleTableExporter()
    print(a.get_values())


@shared_task(bind=True)
def update_currency_rate(self, currency_name: str):
    """ Данные из парсера сохраняет в таблицу последних значений валют  """
    current_currency_rate = usdrub_currency_export(currency_name)
    row_with_needed_currency = CurrenciesRates.objects.filter(currency_name='USD')
    if not row_with_needed_currency:
        CurrenciesRates(
            currency_name='USD',
            rate=current_currency_rate
        ).save()
    else:
        row_with_needed_currency[0].rate = current_currency_rate
        row_with_needed_currency[0].save()
