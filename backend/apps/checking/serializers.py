from rest_framework import serializers
from .models import Check, Person
from django.utils import timezone
from django.db import connection


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


class CheckinsTodaySerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    person_name = serializers.CharField(max_length=255)
    person_document = serializers.CharField(max_length=255)
    check_in = serializers.DateTimeField()
    people_inside_count = serializers.IntegerField()

    def get_people_inside_today(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT count_people_inside_today();")
            result = cursor.fetchone()
        return result[0] if result else 0

    def get_persons_checkins_today(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_persons_checkins_today();")
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return results

    def to_representation(self, instance):
        people_inside_count = self.get_people_inside_today()
        persons_checkins_today = self.get_persons_checkins_today()

        for person in persons_checkins_today:
            person['people_inside_count'] = people_inside_count
        return persons_checkins_today


class ReportRangeSerializer(serializers.Serializer):
    def get_calculate_hours(self, person_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute("SELECT calculate_hours(%s, %s, %s);", [person_id, start_date, end_date])
            result = cursor.fetchone()
        return result[0] if result else 0

    def get_persons_report_range(self, person_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_checking_reports_range(%s, %s, %s);", [person_id, start_date, end_date])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return results


class ReportAreaRangeSerializer(serializers.Serializer):
    def get_calculate_area_hours(self, person_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute("SELECT calculate_total_hours_area(%s, %s, %s);", [person_id, start_date, end_date])
            result = cursor.fetchone()
        return result[0] if result else 0

    def get_area_report_range(self, person_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_checking_reports_area_range(%s, %s, %s);", [person_id, start_date, end_date])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return results
