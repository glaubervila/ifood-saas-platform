import os

from cryptography.fernet import Fernet
from django.db import models

from ifood_saas.customers.models import Customer

# Chave de criptografia para as credencias.
# Reutilize a mesma instância da chave em tempo de execução
FERNET_KEY = os.environ.get("FERNET_KEY", None)
if not FERNET_KEY:
    msg = "FERNET_KEY environment variable is not set"
    raise ValueError(msg)
fernet = Fernet(FERNET_KEY.encode())


class Merchant(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="merchants",
    )
    merchant_id = models.UUIDField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=255)
    corporate_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _client_id = models.BinaryField(db_column="client_id")
    _client_secret = models.BinaryField(db_column="client_secret")

    def __str__(self):
        return self.name

    @property
    def client_id(self):
        return fernet.decrypt(self._client_id).decode()

    @client_id.setter
    def client_id(self, value):
        self._client_id = fernet.encrypt(value.encode())

    @property
    def client_secret(self):
        return fernet.decrypt(self._client_secret).decode()

    @client_secret.setter
    def client_secret(self, value):
        self._client_secret = fernet.encrypt(value.encode())
