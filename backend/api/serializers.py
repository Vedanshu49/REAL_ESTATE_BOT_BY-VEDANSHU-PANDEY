from rest_framework import serializers
from .models import Property, Query


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'location', 'property_type', 'price', 'price_per_sqft',
            'area_sqft', 'year', 'demand', 'demand_score', 'created_at'
        ]


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id', 'user_query', 'location_filter', 'response_summary', 'chart_data', 'table_data', 'created_at']


class QueryRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500)
