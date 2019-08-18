from django.contrib import admin

from parties.models import DemoParty, DemoPartyLocation, DemoPartyURL, DemoPartyVisitor, DemoPartySeries

class DemoPartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'series', 'location', 'url', 'demo_party_start', 'demo_party_end']
    search_fields = ['name', 'series__name', 'url__url']

admin.site.register(DemoParty, DemoPartyAdmin)

class DemoPartySeriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(DemoPartySeries, DemoPartySeriesAdmin)

class DemoPartyLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'address1', 'address2', 'postal_code', 'city', 'country', 'latitude', 'longitude']

admin.site.register(DemoPartyLocation, DemoPartyLocationAdmin)

class DemoPartyURLAdmin(admin.ModelAdmin):
    list_display = ['id', 'url']

admin.site.register(DemoPartyURL, DemoPartyURLAdmin)

class DemoPartyVisitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'demo_party', 'status']

admin.site.register(DemoPartyVisitor, DemoPartyVisitorAdmin)