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
    a = usdrub_currency_export(currency_name)
    print(a)
