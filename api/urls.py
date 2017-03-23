# coding=utf-8
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import city_list

__author__ = 'alexy'


urlpatterns = patterns(
    '',
    url(r'^city/$', city_list, name='city-list'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
