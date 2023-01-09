from django.contrib import admin
from django.urls import include, path

from runs import views

urlpatterns = [
    path("runs/", views.RunList.as_view(), name="run-list"),
    path(
        "runs/<str:run_id>/",
        views.RunDetail.as_view(),
        name="run-detail",
    ),
    path("runs/<str:run_id>/status", views.RunStatus.as_view(), name="run-status"),
    path("runs/<str:run_id>/stdout", views.RunStdout.as_view(), name="run-stdout"),
    path("runs/<str:run_id>/stderr", views.RunStderr.as_view(), name="run-stderr"),
]
