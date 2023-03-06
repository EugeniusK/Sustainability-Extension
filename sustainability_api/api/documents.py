from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Activity

@registry.register_document
class ActivityDocument(Document):
    class Index:
        name = 'activities'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
    class Django:
        model = Activity
        fields = [
            'name_category_sector_description', 'region', 'unit_type', 'unit', 'co2e_factor', 'co2', 'ch4', 'n2o'
        ]
