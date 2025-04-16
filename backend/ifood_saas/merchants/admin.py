from django import forms
from django.contrib import admin

from ifood_saas.customers.models import Customer
from ifood_saas.merchants.models import Merchant
from ifood_saas.merchants.models.merchant_access import MerchantAccess


class MerchantAccessInline(admin.TabularInline):
    model = MerchantAccess
    extra = 1
    autocomplete_fields = ["user"]


class MerchantAdminForm(forms.ModelForm):
    client_id = forms.CharField(label="Client ID")
    client_secret = forms.CharField(
        label="Client Secret",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Merchant
        fields = [
            "customer",
            "merchant_id",
            "client_id",
            "client_secret",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["client_id"].initial = self.instance.client_id
            self.fields["client_secret"].initial = self.instance.client_secret

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)
        instance.client_id = self.cleaned_data["client_id"]
        instance.client_secret = self.cleaned_data["client_secret"]
        if commit:
            instance.save()
        return instance


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    form = MerchantAdminForm
    inlines = [MerchantAccessInline]
    list_display = (
        "id",
        "merchant_id",
        "name",
        "corporate_name",
        "customer",
        "created_at",
        "registered_at",
        "updated_at",
    )
    search_fields = ("name", "corporate_name")
    list_filter = ("registered_at",)
    ordering = ("-registered_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_access__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "customer" and not request.user.is_superuser:
            kwargs["queryset"] = Customer.objects.filter(pk=request.user.customer_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MerchantAccess)
class MerchantAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "merchant", "get_customer")
    search_fields = ("user__username", "merchant__name", "merchant__corporate_name")
    list_filter = ("merchant__customer",)

    @admin.display(
        description="Customer",
    )
    def get_customer(self, obj):
        return obj.merchant.customer

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(merchant__customer_id=request.user.customer_id)
