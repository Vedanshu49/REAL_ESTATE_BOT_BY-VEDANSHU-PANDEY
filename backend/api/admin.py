from django.contrib import admin
from .models import Property, Query


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('location', 'property_type', 'price', 'year', 'demand_score')
    list_filter = ('location', 'property_type', 'year')
    search_fields = ('location',)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('user_query', 'location_filter', 'created_at')
    list_filter = ('created_at', 'location_filter')
    search_fields = ('user_query', 'location_filter')
    readonly_fields = ('response_summary', 'chart_data', 'table_data')
