from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workflows import views

urlpatterns = [
    path(
        "<str:username>/workflows", views.WorkflowList.as_view(), name="workflow-list"
    ),
    path(
        "<str:username>/workflows/<str:workflow_id>/",
        views.WorkflowDetail.as_view(),
        name="workflow-detail",
    ),
    path(
        "<str:username>/workflows/<str:workflow_id>/workflow",
        views.WorkflowFile.as_view(),
        name="workflow-file",
    ),
]
