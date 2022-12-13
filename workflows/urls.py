from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workflows import views

router = DefaultRouter()
router.register("workflows", views.WorkflowViewSet, basename="workflow")

urlpatterns = router.urls
