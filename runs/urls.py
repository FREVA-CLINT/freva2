from django.contrib import admin
from rest_framework.routers import DefaultRouter

from runs import views

router = DefaultRouter()
router.register("runs", views.RunViewSet, basename="runs")

urlpatterns = router.urls
