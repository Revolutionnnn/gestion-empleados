from rest_framework import generics
from .models import Area, Person
from . import serializers
from server.protect import ProtectRelatedDeleteMixin


class AreaListCreateView(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerializer
    search_fields = ['name']


class AreaUpdateDeleteView(ProtectRelatedDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerializer
    lookup_field = 'uuid'


class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = serializers.PersonListSerializer
    search_fields = ['name', 'document']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PersonSerializer
        return serializers.PersonListSerializer


class PersonUpdateDeleteView(ProtectRelatedDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer
    lookup_field = 'uuid'
