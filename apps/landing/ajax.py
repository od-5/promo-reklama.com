# coding=utf-8
import urllib
import urlparse
import urllib2
import json

from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from core.models import Setup

from .models import City

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def ticket(request):
    name = request.POST.get('name') or ''
    phone = request.POST.get('phone') or ''
    mail = request.POST.get('mail') or ''
    theme = request.POST.get('theme') or ''
    city = request.POST.get('city') or ''
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
    values = {
        'name': name.encode('utf-8'),
        'phone': phone.encode('utf-8'),
        'mail': mail.encode('utf-8'),
        'theme': theme.encode('utf-8'),
        'city': city.encode('utf-8')
    }
    data = urllib.urlencode(values)
    req = urllib2.Request('http://reklamadoma.com/ticket/promo/', data, headers)
    response = urllib2.urlopen(req)
    answer = json.load(response)
    if answer['success']:
        return {
            'success': True,
            'name': name,
            'phone': phone,
            'mail': mail,
            'theme': theme
        }
    return {
        'success': False
    }


@csrf_exempt
@ajax_request
def find_city(request):
    if request.GET.get('name_startsWith'):
        name_startsWith = request.GET.get('name_startsWith')
        city_list = []
        city_qs = City.objects.filter(name__icontains=name_startsWith)
        for city in city_qs:
            city_list.append({
                'name': city.name
            })
        return {
            'city_list': city_list
        }
    return {
        'success': True
    }
