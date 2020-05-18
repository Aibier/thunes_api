from apps.accounts.models import Currencies
from .currencies import CURRENCIES as currencies

def sync_currencies():
	Currencies.objects.all().delete()
	for cur in currencies:
		Currencies.objects.create(code=cur['code'], name=cur['name'], symbol=cur['symbol'])