from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import College, OrgMember, Organization, Program, Student


def home(request):
    context = {
        "college_count": College.objects.count(),
        "program_count": Program.objects.count(),
        "organization_count": Organization.objects.count(),
        "student_count": Student.objects.count(),
        "orgmember_count": OrgMember.objects.count(),
        "recent_organizations": Organization.objects.select_related("college").order_by("-created_at")[:6],
        "recent_students": Student.objects.select_related("program", "program__college").order_by("-created_at")[:8],
    }
    return render(request, "studentorg/home.html", context)


def _paginate(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def college_list(request):
    query = request.GET.get("q", "").strip()
    colleges = College.objects.all().order_by("college_name")

    if query:
        colleges = colleges.filter(college_name__icontains=query)

    page_obj = _paginate(request, colleges)

    return render(
        request,
        "studentorg/college_list.html",
        {
            "page_obj": page_obj,
            "q": query,
        },
    )


def program_list(request):
    query = request.GET.get("q", "").strip()
    programs = Program.objects.select_related("college").all().order_by("prog_name")

    if query:
        programs = programs.filter(Q(prog_name__icontains=query) | Q(college__college_name__icontains=query))

    page_obj = _paginate(request, programs)
    return render(request, "studentorg/program_list.html", {"page_obj": page_obj, "q": query})


def organization_list(request):
    query = request.GET.get("q", "").strip()
    organizations = Organization.objects.select_related("college").all().order_by("name")

    if query:
        organizations = organizations.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(college__college_name__icontains=query)
        )

    page_obj = _paginate(request, organizations)
    return render(request, "studentorg/organization_list.html", {"page_obj": page_obj, "q": query})


def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.select_related("program", "program__college").all().order_by("lastname", "firstname")

    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(lastname__icontains=query)
            | Q(firstname__icontains=query)
            | Q(program__prog_name__icontains=query)
        )

    page_obj = _paginate(request, students)
    return render(request, "studentorg/student_list.html", {"page_obj": page_obj, "q": query})


def orgmember_list(request):
    query = request.GET.get("q", "").strip()
    orgmembers = OrgMember.objects.select_related("student", "student__program", "student__program__college", "organization").all().order_by(
        "-date_joined"
    )

    if query:
        orgmembers = orgmembers.filter(
            Q(student__student_id__icontains=query)
            | Q(student__lastname__icontains=query)
            | Q(student__firstname__icontains=query)
            | Q(organization__name__icontains=query)
        )

    page_obj = _paginate(request, orgmembers)
    return render(request, "studentorg/orgmember_list.html", {"page_obj": page_obj, "q": query})
