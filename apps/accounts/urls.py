from django.conf.urls import url, include
from .views import ThunesUserAccountAPI, ThunesTransactionViewSet, ThunesUserAccountTopupAPI, ThunesTransactionReportAPI
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Account API')

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', ThunesTransactionViewSet, basename='transactions')

urlpatterns = [
    url(r'^$', ThunesUserAccountAPI.as_view(), name='account_create'),
    url(r'^topup/$', ThunesUserAccountTopupAPI.as_view(), name='account_topup'),
    url(r'^report/$', ThunesTransactionReportAPI.as_view(), name='report'),
    url(r'^', include(router.urls)),
]