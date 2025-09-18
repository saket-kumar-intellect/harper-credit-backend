from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Application
from core.serializers import ApplicationCreateSerializer, ApplicationDetailSerializer


class ApplicationListCreateView(APIView):
    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        detail = ApplicationDetailSerializer(application)
        return Response(detail.data, status=status.HTTP_201_CREATED)


class ApplicationDetailView(APIView):
    def get(self, request, pk: int):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationDetailSerializer(application)
        return Response(serializer.data)


