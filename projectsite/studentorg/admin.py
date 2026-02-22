from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname", "firstname", "middlename", "program")
    list_filter = ("program",)
    search_fields = ("student_id", "lastname", "firstname")


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "organization", "date_joined")
    list_filter = ("organization",)
    search_fields = ("student__lastname", "student__firstname", "organization__name")


admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)