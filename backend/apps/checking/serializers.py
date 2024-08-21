from rest_framework import serializers
from .models import Check


class CheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = (
            'id',
            'uuid',
            'created',
            'person',
            'check_in',
            'check_out',
            'reason'
        )

    def validate(self, data):
        check_in = data.get('check_in', None)
        check_out = data.get('check_out', None)

        if check_in and check_out:
            delta = check_out - check_in
            hours_worked = delta.total_seconds() / 3600

            if hours_worked < 8 and not data.get('reason'):
                raise serializers.ValidationError(
                    "Si trabajó menos de 8 horas, debe proporcionar un motivo."
                )

        return data
