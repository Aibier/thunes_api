from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Thunes API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.accounts.urls')),
    path('api/auth/', include('apps.authentication.urls'), name='jwtauth'),
    path('api/docs/', schema_view),
]
