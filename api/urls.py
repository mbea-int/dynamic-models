from django.urls import path
from .views import TableApiView

urlpatterns = [
    path('table/', TableApiView.as_view(), name="model")
]