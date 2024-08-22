from rest_framework import serializers
from .models import Check, Person
from django.utils import timezone
from datetime import time


class CheckSerializer(serializers.ModelSerializer):
    document = serializers.CharField(write_only=True)
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), required=False)
    check_in = serializers.DateTimeField(required=False)

    class Meta:
        model = Check
        fields = (
            'id',
            'uuid',
            'created',
            'person',
            'check_in',
            'check_out',
            'reason',
            'document'
        )

    def create(self, validated_data):
        document = validated_data.pop('document')
        reason = validated_data.get('reason')
        person = Person.objects.get(document=document)
        today = timezone.now().date()
        instance_check = Check.objects.filter(person=person, check_in__date=today).last()

        if instance_check and not instance_check.check_out:
            check_out = timezone.now()

            cutoff_time = check_out.replace(hour=16, minute=0, second=0, microsecond=0)
            if check_out < cutoff_time and not reason and person.type == Person.EMPLEYEE:
                raise serializers.ValidationError(
                    "Si está saliendo antes de las 16:00, debe proporcionar un motivo."
                )

            instance_check.check_out = check_out
            instance_check.reason = reason
            instance_check.save()

            validated_data['check_in'] = instance_check.check_in
            validated_data['check_out'] = instance_check.check_out
            validated_data['reason'] = instance_check.reason

            return instance_check

        validated_data['person'] = person
        validated_data['check_in'] = timezone.now()
        return super().create(validated_data)
