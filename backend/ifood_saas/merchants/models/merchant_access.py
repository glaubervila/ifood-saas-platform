from django.core.exceptions import ValidationError
from django.db import models

from ifood_saas.merchants.models import Merchant
from ifood_saas.users.models import User


class MerchantAccess(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="merchant_access",
    )
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="user_access",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "merchant")

    def __str__(self):
        return f"{self.user.username} - {self.merchant.name}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.user.customer != self.merchant.customer:
            msg = "User and merchant must belong to the same customer."
            raise ValidationError(msg)
