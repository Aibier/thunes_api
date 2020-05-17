from django.conf.urls import url
from .views import ThunesUserAccountAPI, ThunesTransactionAPI, ThunesUserAccountTopupAPI
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Account API')

urlpatterns = [
    url(r'^$', ThunesUserAccountAPI.as_view(), name='account_create'),
    url(r'^topup/$', ThunesUserAccountTopupAPI.as_view(), name='account_topup'),
    url(r'^transactions/$', ThunesTransactionAPI.as_view(), name='send_to_user'),
]