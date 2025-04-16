from django.contrib import admin

from ifood_saas.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "corporate_name", "cnpj", "created_at")
    search_fields = ("name", "corporate_name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
