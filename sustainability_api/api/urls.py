from django.urls import path, include
from rest_framework import routers
from .views import ActivityViewSet, ActivityElasticsearchView, ItemView



urlpatterns = [
    path('search/', ActivityElasticsearchView),
    path('item/', ItemView.as_view())
]