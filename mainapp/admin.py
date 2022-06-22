from django.contrib import admin
from .models import ProductTable


@admin.register(ProductTable)
class ProductTableAdmin(admin.ModelAdmin):
    pass

