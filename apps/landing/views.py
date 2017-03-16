# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin
from django_geoip.models import IpRange

from .models import Country, City, Moderator

__author__ = 'alexy'


class CityListMixin(ContextMixin):
    """
    Миксин добавляет список городов в контекст
    """
    def get_context_data(self, **kwargs):
        kwargs = super(CityListMixin, self).get_context_data(**kwargs)
        kwargs.update({'city_list': City.objects.all()})
        return kwargs


class LandingView(TemplateView, CityListMixin):
    template_name = 'index.html'


class CityDetailView(DetailView, CityListMixin):
    model = City
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(CityDetailView, self).get_context_data()
        moderator_qs = Moderator.objects.filter(city=self.object)
        if moderator_qs.count() == 1 and moderator_qs.first().phone:
            context.update({
                'phone': moderator_qs.first().phone
            })
        context.update({
            'moderator_list': moderator_qs
        })
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home_view(request):
    ip = get_client_ip(request)
    try:
        geoip_record = IpRange.objects.by_ip(ip)
        city_name = geoip_record.city.name
        city = get_object_or_None(City, name__iexact=city_name)
        if city:
            return HttpResponseRedirect(reverse('landing:city', args=(city.slug,)))
    except IpRange.DoesNotExist:
        city_name = None
    context = {
        'city_list': City.objects.all(),
        'country_list': Country.objects.all(),
        'location': city_name,
        'ip': ip
    }
    return render(request, 'index.html', context)


def set_current_city_from_input(request):
    if request.POST.get('city'):
        try:
            current_city = City.objects.get(name__iexact=request.POST.get('city'))
            return HttpResponseRedirect(reverse('landing:city', args=(current_city.slug, )))
        except:
            pass
    return HttpResponseRedirect(reverse('landing:index'))
