from django.core.paginator import Paginator
from django.shortcuts import render

from .models import College


def home(request):
    return render(request, "studentorg/home.html")


def college_list(request):
    query = request.GET.get("q", "").strip()
    colleges = College.objects.all().order_by("college_name")

    if query:
        colleges = colleges.filter(college_name__icontains=query)

    paginator = Paginator(colleges, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "studentorg/college_list.html",
        {
            "page_obj": page_obj,
            "q": query,
        },
    )
