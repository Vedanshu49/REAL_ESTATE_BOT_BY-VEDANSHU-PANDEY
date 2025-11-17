from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Property, Query
from .serializers import PropertySerializer, QuerySerializer, QueryRequestSerializer
from .services import GeminiService, DataProcessingService, QueryClassifier
import csv
import json


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        location = request.query_params.get('location')
        if location:
            queryset = self.queryset.filter(location__icontains=location)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'Location parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def locations_list(self, request):
        locations = self.queryset.values_list('location', flat=True).distinct()
        return Response({'locations': list(locations)})


class QueryViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        serializer = QueryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_query = serializer.validated_data['query']
        
        # INTELLIGENT QUERY CLASSIFICATION
        query_type = QueryClassifier.classify(user_query)
        
        # Parse location from query
        parsed = DataProcessingService.parse_query(user_query)
        location = parsed['location']
        
        # Filter properties
        properties = DataProcessingService.filter_properties(location=location)
        
        if not properties.exists():
            return Response({
                'error': f'No properties found for {location if location else "the given criteria"}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Prepare chart and table data
        chart_data = DataProcessingService.prepare_chart_data(properties)
        table_data = DataProcessingService.prepare_table_data(properties)
        
        # INTELLIGENT SUMMARY GENERATION
        gemini_service = GeminiService()
        properties_list = list(properties.values())
        summary = gemini_service.generate_intelligent_summary(
            properties_list, 
            location=location, 
            query=user_query,
            query_type=query_type
        )
        
        # Save query to database
        query_obj = Query.objects.create(
            user_query=user_query,
            location_filter=location or 'all',
            response_summary=summary,
            chart_data=chart_data,
            table_data=table_data
        )
        
        return Response({
            'summary': summary,
            'chartData': chart_data,
            'tableData': table_data,
            'count': len(table_data),
            'queryType': query_type
        })
        
        # Save query to database
        query_obj = Query.objects.create(
            user_query=user_query,
            location_filter=location,
            response_summary=summary,
            chart_data=chart_data,
            table_data=table_data
        )
        
        return Response({
            'summary': summary,
            'chartData': chart_data,
            'tableData': table_data,
            'count': len(table_data)
        })
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        queries = Query.objects.all()[:10]
        serializer = QuerySerializer(queries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def download_data(self, request):
        serializer = QueryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_query = serializer.validated_data['query']
        parsed = DataProcessingService.parse_query(user_query)
        location = parsed['location']
        
        properties = DataProcessingService.filter_properties(location=location)
        
        if not properties.exists():
            return Response({
                'error': 'No properties found for download'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="real_estate_{location or "data"}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Location', 'Type', 'Price', 'Price/Sqft', 'Area (Sqft)', 'Year', 'Demand', 'Demand Score'])
        
        for prop in properties:
            writer.writerow([
                prop.location,
                prop.property_type,
                prop.price,
                prop.price_per_sqft or '',
                prop.area_sqft or '',
                prop.year,
                prop.demand,
                prop.demand_score
            ])
        
        return response
