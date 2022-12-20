from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workflows import views

urlpatterns = [
    path("<str:user_id>/workflows", views.WorkflowList.as_view(), name="workflow-list"),
    path(
        "<str:user_id>/workflows/<str:workflow_id>/",
        views.WorkflowDetail.as_view(),
        name="workflow-detail",
    ),
    path(
        "<str:user_id>/workflows/<str:workflow_id>/workflow",
        views.WorkflowFile.as_view(),
        name="workflow-file",
    ),
]
