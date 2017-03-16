# coding=utf-8
from django.contrib import admin

from .models import Country, City, Moderator

__author__ = 'alexy'


class CountryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('country', )
    fieldsets = (
        (None, {'fields': ('country', 'name', 'slug')}),
        (u'SEO', {'fields': ('meta_title', 'meta_desc', 'meta_key')}),
    )

    def has_add_permission(self, request):
        return False


class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('company', 'phone', 'contact')
    filter_horizontal = ('city', )

    def has_add_permission(self, request):
        return False


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Moderator, ModeratorAdmin)
