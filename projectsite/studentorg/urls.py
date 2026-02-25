from django.urls import path

from .views import (
    CollegeCreateView,
    CollegeDeleteView,
    CollegeList,
    CollegeUpdateView,
    HomePageView,
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationList,
    OrganizationUpdateView,
    OrgMemberCreateView,
    OrgMemberDeleteView,
    OrgMemberList,
    OrgMemberUpdateView,
    ProgramCreateView,
    ProgramDeleteView,
    ProgramList,
    ProgramUpdateView,
    StudentCreateView,
    StudentDeleteView,
    StudentList,
    StudentUpdateView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    path("organization_list/", OrganizationList.as_view(), name="organization-list"),
    path("organization_list/add/", OrganizationCreateView.as_view(), name="organization-add"),
    path("organization_list/<int:pk>/", OrganizationUpdateView.as_view(), name="organization-update"),
    path("organization_list/<int:pk>/delete/", OrganizationDeleteView.as_view(), name="organization-delete"),

    path("college_list/", CollegeList.as_view(), name="college-list"),
    path("college_list/add/", CollegeCreateView.as_view(), name="college-add"),
    path("college_list/<int:pk>/", CollegeUpdateView.as_view(), name="college-update"),
    path("college_list/<int:pk>/delete/", CollegeDeleteView.as_view(), name="college-delete"),

    path("program_list/", ProgramList.as_view(), name="program-list"),
    path("program_list/add/", ProgramCreateView.as_view(), name="program-add"),
    path("program_list/<int:pk>/", ProgramUpdateView.as_view(), name="program-update"),
    path("program_list/<int:pk>/delete/", ProgramDeleteView.as_view(), name="program-delete"),

    path("student_list/", StudentList.as_view(), name="student-list"),
    path("student_list/add/", StudentCreateView.as_view(), name="student-add"),
    path("student_list/<int:pk>/", StudentUpdateView.as_view(), name="student-update"),
    path("student_list/<int:pk>/delete/", StudentDeleteView.as_view(), name="student-delete"),

    path("orgmember_list/", OrgMemberList.as_view(), name="orgmember-list"),
    path("orgmember_list/add/", OrgMemberCreateView.as_view(), name="orgmember-add"),
    path("orgmember_list/<int:pk>/", OrgMemberUpdateView.as_view(), name="orgmember-update"),
    path("orgmember_list/<int:pk>/delete/", OrgMemberDeleteView.as_view(), name="orgmember-delete"),
]
