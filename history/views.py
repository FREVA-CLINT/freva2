from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


def index(request):
    return render(request, "history/index.html", {"title": "History main page"})
