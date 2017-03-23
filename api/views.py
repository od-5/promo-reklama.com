# coding=utf-8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CitySerializer
from apps.landing.models import City

__author__ = 'alexy'


@api_view(['GET'])
def city_list(request, format=None):
    """
    Отображение списка городов
    """
    if request.method == 'GET':
        region = request.GET.get('region', None)
        city_qs = City.objects.all()
        if region and region.isdigit():
            city_qs = city_qs.filter(region=int(region))
        if city_qs:
            serializer = CitySerializer(city_qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
