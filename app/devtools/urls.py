from django.urls import path

from devtools.views import ImportView

app_name = "devtools"

urlpatterns = [
    path('import/', ImportView.as_view(), name="importview")
]
