from .tasks import update_currency_rate, update_table_in_interval
from .models import ProductTable

from django.views.generic import ListView


class MainView(ListView):
    model = ProductTable
    template_name = "main.html"
    queryset = ProductTable.objects.all()


