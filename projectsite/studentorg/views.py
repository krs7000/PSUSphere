from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import CollegeForm, OrganizationForm, OrgMemberForm, ProgramForm, StudentForm
from .models import College, Organization, OrgMember, Program, Student


class HomePageView(TemplateView):
    template_name = "studentorg/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "college_count": College.objects.count(),
                "program_count": Program.objects.count(),
                "organization_count": Organization.objects.count(),
                "student_count": Student.objects.count(),
                "orgmember_count": OrgMember.objects.count(),
                "recent_organizations": Organization.objects.select_related("college").order_by("-created_at")[:6],
                "recent_students": Student.objects.select_related("program", "program__college").order_by(
                    "-created_at"
                )[:8],
            }
        )
        return context


class BaseSearchListView(ListView):
    paginate_by = 10
    search_fields = ()

    def get_search_query(self):
        return self.request.GET.get("q", "").strip()

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.get_search_query()
        if not q or not self.search_fields:
            return queryset

        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": q})
        return queryset.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.get_search_query()
        return context


class OrganizationList(BaseSearchListView):
    model = Organization
    template_name = "studentorg/org_list.html"
    paginate_by = 5
    search_fields = ("name", "college__college_name", "description")

    def get_queryset(self):
        return super().get_queryset().select_related("college").order_by("name")


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "studentorg/org_form.html"
    success_url = reverse_lazy("organization-list")


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "studentorg/org_form.html"
    success_url = reverse_lazy("organization-list")


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = "studentorg/org_del.html"
    success_url = reverse_lazy("organization-list")


class CollegeList(BaseSearchListView):
    model = College
    template_name = "studentorg/college_list.html"
    paginate_by = 10
    search_fields = ("college_name",)

    def get_queryset(self):
        return super().get_queryset().order_by("college_name")


class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = "studentorg/college_form.html"
    success_url = reverse_lazy("college-list")


class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = "studentorg/college_form.html"
    success_url = reverse_lazy("college-list")


class CollegeDeleteView(DeleteView):
    model = College
    template_name = "studentorg/college_del.html"
    success_url = reverse_lazy("college-list")


class ProgramList(BaseSearchListView):
    model = Program
    template_name = "studentorg/program_list.html"
    paginate_by = 10
    search_fields = ("prog_name", "college__college_name")

    def get_queryset(self):
        return super().get_queryset().select_related("college").order_by("prog_name")


class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "studentorg/program_form.html"
    success_url = reverse_lazy("program-list")


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "studentorg/program_form.html"
    success_url = reverse_lazy("program-list")


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "studentorg/program_del.html"
    success_url = reverse_lazy("program-list")


class StudentList(BaseSearchListView):
    model = Student
    template_name = "studentorg/student_list.html"
    paginate_by = 10
    search_fields = ("student_id", "lastname", "firstname", "program__prog_name")

    def get_queryset(self):
        return super().get_queryset().select_related("program", "program__college").order_by("lastname", "firstname")


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "studentorg/student_form.html"
    success_url = reverse_lazy("student-list")


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "studentorg/student_form.html"
    success_url = reverse_lazy("student-list")


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "studentorg/student_del.html"
    success_url = reverse_lazy("student-list")


class OrgMemberList(BaseSearchListView):
    model = OrgMember
    template_name = "studentorg/orgmember_list.html"
    paginate_by = 10
    search_fields = ("student__student_id", "student__lastname", "student__firstname", "organization__name")

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("student", "student__program", "student__program__college", "organization")
            .order_by("-date_joined")
        )


class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = "studentorg/orgmember_form.html"
    success_url = reverse_lazy("orgmember-list")


class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = "studentorg/orgmember_form.html"
    success_url = reverse_lazy("orgmember-list")


class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = "studentorg/orgmember_del.html"
    success_url = reverse_lazy("orgmember-list")
