# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models

from core.base_model import CommonPage

__author__ = 'alexy'


class CountryManager(models.Manager):

    @staticmethod
    def get_id_list():
        id_list = [int(i.id) for i in Country.objects.all()]
        return id_list


class RegionManager(models.Manager):

    @staticmethod
    def get_id_list():
        id_list = [int(i.id) for i in Region.objects.all()]
        return id_list


class CityManager(models.Manager):

    @staticmethod
    def get_id_list():
        id_list = [int(i.id) for i in City.objects.all()]
        return id_list


class ModeratorManager(models.Manager):

    @staticmethod
    def get_id_list():
        id_list = [int(i.id) for i in Moderator.objects.all()]
        return id_list


class Country(models.Model):
    class Meta:
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'
        app_label = 'landing'

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name=u'Название')
    objects = CountryManager()


class Region(models.Model):
    class Meta:
        verbose_name = u'Регион'
        verbose_name_plural = u'Регионы'
        app_label = 'landing'

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name=u'Название')
    country = models.ForeignKey(Country, verbose_name=u'Страна')

    objects = RegionManager()


class City(CommonPage):
    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'
        app_label = 'landing'
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('landing:city', args=(self.slug,))

    country = models.ForeignKey(to=Country, verbose_name=u'Страна')
    region = models.ForeignKey(to=Region, verbose_name=u'Страна', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name=u'Название')
    slug = models.SlugField(max_length=100, verbose_name=u'URL города')
    objects = CityManager()


class Moderator(models.Model):
    class Meta:
        verbose_name = u'Исполнитель'
        verbose_name_plural = u'Исполнители'
        app_label = 'landing'

    def __unicode__(self):
        return self.company

    def id_list(self):
        return [i.id for i in self.city.all()]

    city = models.ManyToManyField(to=City)
    company = models.CharField(max_length=256, verbose_name=u'Название')
    phone = models.CharField(max_length=256, verbose_name=u'телефон', blank=True, null=True)
    contact = models.TextField(verbose_name=u'контакты', blank=True, null=True)
    objects = ModeratorManager()
