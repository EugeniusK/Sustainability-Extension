from django.shortcuts import render

from django.http import HttpResponse, JsonResponse 
from rest_framework import viewsets, generics
from rest_framework import mixins
from .models import Activity, Cart
from .serializers import ActivitySerializer, ItemSerializer
from .documents import ActivityDocument
import requests
from django.conf import settings


# Create your views here.
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ActivityElasticsearchView(request):
    print(request)
    if request.method == "POST":
        URL = "http://" + settings.ELASTICSEARCH_DSL['default']['hosts'] + '/activities/_search'
        json_data = json.loads(request.body)
        query = json.dumps({
            "size": 1,
            "query": {
                "match": {
                    "name_category_sector_description": json_data['main'],
                },
            }
        })
        r = requests.post(URL, data=query,  headers={'Content-type' :'application/json'}).content
        print(r)
        return JsonResponse(json.loads(r)['hits']['hits'][0]['_source'])
    else:
        return HttpResponse(status=405)
    
class ItemView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = ItemSerializer