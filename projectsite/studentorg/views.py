from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CollegeForm, OrganizationForm, OrgMemberForm, ProgramForm, StudentForm
from .models import College, Organization, OrgMember, Program, Student


class HomePageView(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = "home"
    template_name = "home.html"

    def get_queryset(self):
        return Organization.objects.select_related("college").order_by("-created_at")[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        context["total_organizations"] = Organization.objects.count()
        context["total_programs"] = Program.objects.count()

        today = timezone.now().date()
        context["students_joined_this_year"] = (
            OrgMember.objects.filter(date_joined__year=today.year).values("student").distinct().count()
        )
        return context


class BaseSearchListView(LoginRequiredMixin, ListView):
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
        context["sort_by"] = self.request.GET.get("sort_by", "")
        return context


class OrganizationList(BaseSearchListView):
    model = Organization
    context_object_name = "organization"
    template_name = "org_list.html"
    paginate_by = 5
    ordering = ["college__college_name", "name"]

    def get_queryset(self):
        qs = Organization.objects.select_related("college")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return qs.order_by(*self.ordering)


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "studentorg/org_form.html"
    success_url = reverse_lazy("organization-list")


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "studentorg/org_form.html"
    success_url = reverse_lazy("organization-list")


class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
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


class CollegeCreateView(LoginRequiredMixin, CreateView):
    model = College
    form_class = CollegeForm
    template_name = "studentorg/college_form.html"
    success_url = reverse_lazy("college-list")


class CollegeUpdateView(LoginRequiredMixin, UpdateView):
    model = College
    form_class = CollegeForm
    template_name = "studentorg/college_form.html"
    success_url = reverse_lazy("college-list")


class CollegeDeleteView(LoginRequiredMixin, DeleteView):
    model = College
    template_name = "studentorg/college_del.html"
    success_url = reverse_lazy("college-list")


class ProgramList(BaseSearchListView):
    model = Program
    context_object_name = "program"
    template_name = "program_list.html"
    paginate_by = 5
    search_fields = ("prog_name", "college__college_name")

    def get_ordering(self):
        allowed = ["prog_name", "college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "prog_name"

    def get_queryset(self):
        return super().get_queryset().select_related("college").order_by(self.get_ordering())


class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "studentorg/program_form.html"
    success_url = reverse_lazy("program-list")


class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "studentorg/program_form.html"
    success_url = reverse_lazy("program-list")


class ProgramDeleteView(LoginRequiredMixin, DeleteView):
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


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "studentorg/student_form.html"
    success_url = reverse_lazy("student-list")


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "studentorg/student_form.html"
    success_url = reverse_lazy("student-list")


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "studentorg/student_del.html"
    success_url = reverse_lazy("student-list")


class OrgMemberList(BaseSearchListView):
    model = OrgMember
    template_name = "studentorg/orgmember_list.html"
    paginate_by = 10
    search_fields = ("student__student_id", "student__lastname", "student__firstname", "organization__name")

    def get_ordering(self):
        allowed = ("student__lastname", "date_joined", "-date_joined")
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "-date_joined"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("student", "student__program", "student__program__college", "organization")
            .order_by(self.get_ordering())
        )


class OrgMemberCreateView(LoginRequiredMixin, CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = "studentorg/orgmember_form.html"
    success_url = reverse_lazy("orgmember-list")


class OrgMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = "studentorg/orgmember_form.html"
    success_url = reverse_lazy("orgmember-list")


class OrgMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = OrgMember
    template_name = "studentorg/orgmember_del.html"
    success_url = reverse_lazy("orgmember-list")
