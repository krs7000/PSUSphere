from django.contrib import admin
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("studentorg.urls")),
]

if settings.ALLAUTH_ENABLED:
    urlpatterns.insert(1, path("accounts/", include("allauth.urls")))
