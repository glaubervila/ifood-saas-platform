from django import forms
from django.contrib import admin

from ifood_saas.merchants.models import Merchant


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
