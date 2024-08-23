from rest_framework import generics
from .models import Check
from . import serializers
from rest_framework.response import Response
from rest_framework import status


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


class ReportRangeAPIView(generics.ListAPIView):
    serializer_class = serializers.ReportRangeSerializer

    def list(self, request, *args, **kwargs):
        person_id = request.query_params.get('id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not person_id or not start_date or not end_date:
            return Response(
                {"detail": "Los campos 'id', 'start_date', y 'end_date' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer()
        start_date = f'{start_date} 00:00:00'
        end_date = f'{end_date} 23:59:59'
        total_hours = serializer.get_calculate_hours(person_id, start_date, end_date)
        report_range = serializer.get_persons_report_range(person_id, start_date, end_date)

        for report in report_range:
            report['total_hours'] = f"{total_hours}"
        return Response(report_range, status=status.HTTP_200_OK)
    

class ReportAreaRangeAPIView(generics.ListAPIView):
    serializer_class = serializers.ReportAreaRangeSerializer

    def list(self, request, *args, **kwargs):
        person_id = request.query_params.get('id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not person_id or not start_date or not end_date:
            return Response(
                {"detail": "Los campos 'id', 'start_date', y 'end_date' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer()
        start_date = f'{start_date} 00:00:00'
        end_date = f'{end_date} 23:59:59'
        total_hours = serializer.get_calculate_area_hours(person_id, start_date, end_date)
        report_range = serializer.get_area_report_range(person_id, start_date, end_date)

        for report in report_range:
            report['total_hours'] = f"{total_hours}"
        return Response(report_range, status=status.HTTP_200_OK)
