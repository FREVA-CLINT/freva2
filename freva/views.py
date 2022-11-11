from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html", {"title": "Freva main page"})


@api_view(["GET"])
@login_required()
def get_json(_request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "Hello": "World",
        },
        status=200,
    )
