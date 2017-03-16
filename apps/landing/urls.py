# coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import LandingView, CityDetailView, set_current_city_from_input
from .ajax import ticket, find_city

__author__ = 'alexy'


urlpatterns = patterns(
    'apps.landing.views',
    url(r'^$', 'home_view', name='index'),
    url(r'^(?P<slug>[\w-]+)$', CityDetailView.as_view(), name='city'),
    url(r'^thnx/$', TemplateView.as_view(template_name='ok.html'), name='thnx'),
    # url(r'^mail/$', TemplateView.as_view(template_name='landing/mail.html'), name='mail'),
    url(r'^ticket/$', ticket, name='ticket'),
    url(r'^fund_city/$', find_city, name='find-city'),
    url(r'^set_city/$', set_current_city_from_input, name='set-city'),
)
