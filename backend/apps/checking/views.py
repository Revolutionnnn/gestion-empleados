from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person, Check
from .serializers import CheckSerializer


class CheckAPIView(APIView):

    def get_person(self, document):
        return get_object_or_404(Person, document=document)

    def get_today_check(self, person):
        today = datetime.now().date()
        return Check.objects.filter(person=person, check_in__date=today).last()

    def get(self, request, document):
        person = self.get_person(document)
        today_check = self.get_today_check(person)

        if not today_check:
            return Response({'detail': 'No check-in found for today.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CheckSerializer(today_check)
        return Response(serializer.data)

    def post(self, request, document):
        person = self.get_person(document)
        today_check = self.get_today_check(person)

        if today_check and today_check.check_out is None:
            return Response({'detail': 'You must check out before creating a new check-in for today.'}, status=status.HTTP_400_BAD_REQUEST)

        check_data = {
            'person': person.id,
            'check_in': datetime.now(),
        }
        serializer = CheckSerializer(data=check_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, document):
        person = self.get_person(document)
        today_check = self.get_today_check(person)

        if not today_check or today_check.check_out:
            return Response({'detail': 'No open check-in found for today to update.'}, status=status.HTTP_404_NOT_FOUND)

        today_check.check_out = datetime.now()
        today_check.save()
        serializer = CheckSerializer(today_check)
        return Response(serializer.data)
