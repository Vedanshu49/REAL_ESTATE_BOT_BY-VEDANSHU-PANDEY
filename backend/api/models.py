from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ]
    
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    area_sqft = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    year = models.IntegerField()
    demand = models.IntegerField(default=0)
    demand_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'location']
        indexes = [
            models.Index(fields=['location', 'year']),
            models.Index(fields=['property_type']),
        ]
    
    def __str__(self):
        return f"{self.location} - {self.property_type} ({self.year})"


class Query(models.Model):
    user_query = models.TextField()
    location_filter = models.CharField(max_length=255, null=True, blank=True)
    response_summary = models.TextField()
    chart_data = models.JSONField()
    table_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query: {self.user_query[:50]}..."
