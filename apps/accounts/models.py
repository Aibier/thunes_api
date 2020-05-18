import uuid
from enumfields import Enum, EnumField
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class TransactionStatuses(Enum):
    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'


class TransactionTypes(Enum):
    EMAIL = 'EMAIL'
    ACCOUNT = 'ACCOUNT'


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_modified_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Currencies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField(unique=True)
    name = models.TextField(blank=False)
    symbol = models.TextField(blank=False)

    class Meta:
        db_table = 'currencies'


class UserAccount(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_account')
    currency = models.OneToOneField(Currencies, on_delete=models.CASCADE, blank=False, related_name='user_account_currency')
    account = models.IntegerField()
    balance = models.DecimalField(max_digits=20, decimal_places=4)
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return 'Account number: {}'.format(self.account)

    class Meta:
        db_table = 'user_account'
    

class Transaction(BaseModel):
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', blank=False, null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    status = EnumField(TransactionStatuses, null=False)
    type = EnumField(TransactionTypes, null=False)

    class Meta:
        db_table = 'trnasactions'


