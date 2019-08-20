from django.http import HttpResponse
from django.views.generic import TemplateView, View

from devtools.parsers import import_demo_party


class ImportView(TemplateView):
    template_name = 'devtools/import.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def post(self, request, *args, **kwargs):
        print("REQUEST POST", request.POST)
        slug = request.POST.get("demopartyslug")
        res = import_demo_party(slug)
        return HttpResponse(res)
