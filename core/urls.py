from django.urls import path

from core.views import ApplicationListCreateView, ApplicationDetailView


urlpatterns = [
    path("applications", ApplicationListCreateView.as_view(), name="application-create"),
    path("applications/<int:pk>", ApplicationDetailView.as_view(), name="application-detail"),
]


