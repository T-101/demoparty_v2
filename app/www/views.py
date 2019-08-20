from django.conf import settings
from django.views.generic import TemplateView

from parties.models import DemoParty


class POCIndexView(TemplateView):
    template_name = 'www/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        if 'slug' in kwargs:
            ctx['party'] = DemoParty.objects.get(slug=kwargs.get('slug'))
        else:
            ctx['parties'] = DemoParty.objects.order_by('demo_party_start')
        return ctx
