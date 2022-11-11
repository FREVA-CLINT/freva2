from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "history/index.html", {"title": "History main page"})
