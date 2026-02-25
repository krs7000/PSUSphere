from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("colleges/", views.college_list, name="college_list"),
    path("programs/", views.program_list, name="program_list"),
    path("organizations/", views.organization_list, name="organization_list"),
    path("students/", views.student_list, name="student_list"),
    path("orgmembers/", views.orgmember_list, name="orgmember_list"),
]
