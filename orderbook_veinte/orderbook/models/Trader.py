from django.contrib.auth.models import AbstractUser

from django.db import models


class AbstractTrader(AbstractUser):
    trader_id = models.CharField(primary_key=True , max_length=255)
    type_token = models.CharField(max_length=255)
    verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    token = models.TextField()
    class Meta:
        abstract = True