from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.shortcuts import redirect, render

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("studentorg.urls")),
]

if settings.ALLAUTH_ENABLED:
    from allauth.socialaccount.providers.google.views import oauth2_callback

    def google_callback_entry(request, *args, **kwargs):
        # If callback is opened directly (no OAuth params), restart login flow.
        if "code" not in request.GET and "error" not in request.GET:
            return redirect("/accounts/google/login/")
        return oauth2_callback(request, *args, **kwargs)

    urlpatterns.insert(1, path("accounts/google/login/callback/", google_callback_entry))
    urlpatterns.insert(2, path("accounts/", include("allauth.urls")))
else:
    def social_unavailable(request):
        return render(request, "socialaccount/unavailable.html", status=503)

    urlpatterns.insert(1, path("accounts/google/login/callback/", social_unavailable))
    urlpatterns.insert(2, path("accounts/google/login/", social_unavailable))
    urlpatterns.insert(3, path("accounts/login/", social_unavailable))
