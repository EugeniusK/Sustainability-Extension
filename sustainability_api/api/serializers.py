from rest_framework import routers, serializers, viewsets
from .models import Activity, Cart
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from api.documents import ActivityDocument

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class ActivityDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ActivityDocument
        fields = [
            'uuid', 'name', 'category','sector', 'year','region','description','unit_type','unit', 'co2e_factor', 'co2', 'ch4' ,'n2o'
        ]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'