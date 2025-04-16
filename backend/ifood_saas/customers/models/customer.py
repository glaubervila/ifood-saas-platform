import uuid

from django.db import models


class Customer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    corporate_name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
