from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # type: ignore [misc]
        context = super().get_context_data(**kwargs)
        context["title"] = "Freva main page"
        context["menu"] = settings.MENU_ENTRIES
        return context


def error_404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    Renders the 404-page. It actually just renders the react-SPA
    but since the react-stuff has its' own Router it will figure
    it out what it has to display.
    We need to define it so that it looks nice to the user and
    provides a proper status-code.
    This page is not visible in debug-mode as Django renders its
    own page then to provide more meaningful information. Change
    to DEBUG = False if you want to see this page.
    """
    return render(
        request,
        "index.html",
        {"title": "404 - Not found", "menu": settings.MENU_ENTRIES},
        status=404,
    )
