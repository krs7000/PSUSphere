<<<<<<< HEAD
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import College, Program, Organization, Student, OrgMember


def home(request):
    return render(request, "studentorg/home.html")


def college_list(request):
    q = request.GET.get("q", "").strip()
    qs = College.objects.all().order_by("college_name")

    if q:
        qs = qs.filter(college_name__icontains=q)

    paginator = Paginator(qs, 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "studentorg/college_list.html", {
        "page_obj": page_obj,
        "q": q,
    })
=======
from django.shortcuts import render
from django.views.generic.list import ListView
from studentorg.models import Organization

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"
>>>>>>> cc8f65327c20e8f3fb0485f68cda231dcbfe5b10
