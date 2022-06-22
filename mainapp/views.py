from django.views.generic import TemplateView
from .tasks import update_currency_rate, update_table_in_interval


class MainView(TemplateView):
    template_name = "main.html"

    def get(self, *args, **kwargs):
        update_table_in_interval.delay()
        return super().get(*args, **kwargs)
