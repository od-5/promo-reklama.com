# coding=utf-8
from rest_framework import serializers

from apps.landing.models import City

__author__ = 'alexy'


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализация модели города
    """
    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'slug',
            'region',
            'country',
            'get_absolute_url'
        )
