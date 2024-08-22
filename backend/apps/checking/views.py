from rest_framework import generics
from .models import Check
from . import serializers
from rest_framework.response import Response


class CheckingListCreateView(generics.ListCreateAPIView):
    queryset = Check.objects.all()
    serializer_class = serializers.CheckSerializer

    def create(self, request, *args, **kwargs):
        document = self.kwargs.get('document')

        mutable_data = request.data.copy()
        mutable_data['document'] = document

        request._full_data = mutable_data

        return super().create(request, *args, **kwargs)


class CheckinsTodayListView(generics.ListAPIView):
    serializer_class = serializers.CheckinsTodaySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        data = serializer.to_representation(None)
        return Response(data)
