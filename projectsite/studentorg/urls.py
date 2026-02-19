from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("colleges/", views.college_list, name="college_list"),
]
