from django.contrib import admin
from .models import ProductTable, CurrenciesRates, ProductTableHash


@admin.register(ProductTable)
class ProductTableAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrenciesRates)
class CurrenciesRatesAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductTableHash)
class ProductTableHashAdmin(admin.ModelAdmin):
    pass
