from django.contrib import admin
from .models import ProductTable, CurrenciesRates


@admin.register(ProductTable)
class ProductTableAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrenciesRates)
class CurrenciesRatesAdmin(admin.ModelAdmin):
    pass
