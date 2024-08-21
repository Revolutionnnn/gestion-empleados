from rest_framework import serializers
from .models import Area, Person


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('uuid', 'created', 'name', 'description')


class PersonListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

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
            'bussines',
            'is_active'
        )

    def get_type(self, obj):
        return {
            'code': self.type,
            'description': obj.get_metodo_pago_display()
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
            'bussines',
            'is_active'
        )
