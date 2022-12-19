from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {"title": "Freva main page", "menu": settings.MENU_ENTRIES},
    )


@api_view(["GET"])
@login_required()
def get_json(_request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "Hello": "World",
        },
        status=200,
    )
