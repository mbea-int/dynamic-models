from rest_framework import serializers
from .models import ModelSchema

TYPE_CHOICES = ['string', 'number', 'boolean']


class FieldsRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=TYPE_CHOICES, default="string")

class TableRequestSerializer(serializers.Serializer):
    table_name = serializers.CharField(max_length=255)
    fields = FieldsRequestSerializer(many=True)