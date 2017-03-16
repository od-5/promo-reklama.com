# coding=utf-8
import requests
import json

from annoying.functions import get_object_or_None
from pytils.translit import slugify

from django.core.management.base import BaseCommand, CommandError

from apps.landing.models import Country, City, Moderator

__author__ = 'alexy'


def delete_difference_element(req_list, model):
    dif_list = list(set(model.objects.get_id_list()).difference(req_list))
    if dif_list:
        model.objects.filter(pk__in=dif_list).delete()
    return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'http://reklamadoma.com/api_promo/%s/'
        country_response = requests.get(url % 'country')
        city_response = requests.get(url % 'city')
        moderator_response = requests.get(url % 'moderator')
        if country_response.status_code == 200 and city_response.status_code == 200 and \
                        moderator_response.status_code == 200:
            country_list = json.loads(country_response.content)
            delete_difference_element([i['id'] for i in country_list], Country)
            for item in country_list:
                country = get_object_or_None(Country, id=item['id'])
                if not country:
                    Country.objects.create(id=item['id'], name=item['name'])
                else:
                    if country.name != item['name']:
                        country.name = item['name']
                        country.save()
                        # print u'id=%s, name=%s' % (country['id'], country['name'])
            city_list = json.loads(city_response.content)
            delete_difference_element([i['id'] for i in city_list], City)
            for item in city_list:
                city = get_object_or_None(City, id=item['id'])
                if not city:
                    City.objects.create(id=item['id'], name=item['name'],
                                        country=Country.objects.get(pk=item['country']), slug=slugify(item['name']))
                else:
                    if city.name != item['name']:
                        city.name = item['name']
                        city.slug = slugify(item['name'])
                        city.save()
            moderator_list = json.loads(moderator_response.content)
            delete_difference_element([i['id'] for i in moderator_list], Moderator)
            for item in moderator_list:
                moderator = get_object_or_None(Moderator, id=item['id'])
                if not moderator:
                    moderator = Moderator.objects.create(id=item['id'], company=item['company'], phone=item['phone'],
                                                         contact=item['contact'])
                    for city in City.objects.filter(pk__in=item['city']):
                        moderator.city.add(city)
                else:
                    if moderator.company != item['company']:
                        moderator.company = item['company']
                    if moderator.phone != item['phone']:
                        moderator.phone = item['phone']
                    if moderator.contact != item['contact']:
                        moderator.contact = item['contact']
                    if moderator.id_list() != item['city']:
                        moderator.city.clear()
                        for city in City.objects.filter(pk__in=item['city']):
                            moderator.city.add(city)
                    moderator.save()
        else:
            print 'country: %s' % country_response.status_code
            print 'city: %s' % city_response.status_code
            print 'moderator: %s' % moderator_response.status_code
