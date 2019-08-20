from django.urls import path

from www.views import POCIndexView

app_name = "www"

urlpatterns = [
    path('', POCIndexView.as_view(), name="poc-index-view"),
    path('<slug:slug>/', POCIndexView.as_view(), name="poc-index-view")
]
