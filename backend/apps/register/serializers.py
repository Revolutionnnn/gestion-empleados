from rest_framework import serializers
from .models import Area, Person


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('id', 'uuid', 'created', 'name', 'description')


class PersonListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    area = AreaSerializer()

    class Meta:
        model = Person
        fields = (
            'id',
            'uuid',
            'created',
            'name',
            'type',
            'phone',
            'area',
            'document',
            'rol',
            'business',
            'is_active'
        )

    def get_type(self, obj):
        return {
            'code': obj.type,
            'description': obj.get_type_display()
        }


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'uuid',
            'created',
            'name',
            'type',
            'phone',
            'area',
            'document',
            'rol',
            'business',
            'is_active'
        )
