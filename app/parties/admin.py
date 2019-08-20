from django.contrib import admin

from parties.models import DemoParty, DemoPartyLocation, DemoPartyExternalURL, DemoPartyVisitor, DemoPartySeries


class DemoPartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'series', 'slug', 'location', 'url', 'demo_party_start', 'demo_party_end', 'created_at',
                    'updated_at']
    search_fields = ['name', 'series__name', 'url__url']


admin.site.register(DemoParty, DemoPartyAdmin)


class DemoPartySeriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(DemoPartySeries, DemoPartySeriesAdmin)


class DemoPartyLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'address_extra', 'postal_code', 'city', 'country', 'latitude', 'longitude']


admin.site.register(DemoPartyLocation, DemoPartyLocationAdmin)


class DemoPartyExternalURLAdmin(admin.ModelAdmin):
    list_display = ['id', 'url']


admin.site.register(DemoPartyExternalURL, DemoPartyExternalURLAdmin)


class DemoPartyVisitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'demo_party', 'status']


admin.site.register(DemoPartyVisitor, DemoPartyVisitorAdmin)
