from django.contrib import admin
from .models import UserAccount, Transaction

admin.site.register(UserAccount)
admin.site.register(Transaction)