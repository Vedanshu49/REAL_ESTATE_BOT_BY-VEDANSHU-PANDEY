import google.generativeai as genai
from django.conf import settings
import json
from django.db.models import Avg, Count, Sum, Q
from .models import Property
from collections import defaultdict


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_intelligent_summary(self, properties_data, location=None, query=None, query_type=None):
        """Generate intelligent summaries based on query type"""
        try:
            if not properties_data:
                return "No data available for the given query."
            
            # Handle different query types
            if query_type == 'listing':
                return self._format_property_listing(properties_data, location)
            elif query_type == 'comparison':
                return self._generate_comparison_analysis(properties_data, location, query)
            elif query_type == 'trend':
                return self._generate_trend_analysis(properties_data, location, query)
            elif query_type == 'recommendation':
                return self._generate_recommendations(properties_data, location, query)
            else:
                return self._generate_general_analysis(properties_data, location, query)
        
        except Exception as e:
            return f"Summary generated with data from {len(properties_data)} properties."
    
    def _format_property_listing(self, properties_data, location=None):
        """Format properties as a clean listing"""
        summary = f"**Properties in {location or 'Database'}** ({len(properties_data)} total)\n\n"
        
        by_type = defaultdict(list)
        for prop in properties_data:
            by_type[prop.get('property_type', 'Residential')].append(prop)
        
        for ptype, props in sorted(by_type.items()):
            summary += f"**{ptype}** ({len(props)})\n"
            for i, prop in enumerate(props, 1):
                summary += f"{i}. {prop.get('location', 'N/A')} | Year: {prop.get('year')} | Price: ${prop.get('price', 0):,.0f} | Demand: {prop.get('demand_score', 0):.0f}\n"
            summary += "\n"
        
        # Add summary stats
        prices = [float(p.get('price', 0)) for p in properties_data if p.get('price')]
        demands = [float(p.get('demand_score', 0)) for p in properties_data if p.get('demand_score')]
        
        if prices:
            summary += "**Summary Stats:**\n"
            summary += f"- Avg Price: ${sum(prices)/len(prices):,.0f}\n"
            summary += f"- Price Range: ${min(prices):,.0f} - ${max(prices):,.0f}\n"
            summary += f"- Avg Demand: {sum(demands)/len(demands):.0f}\n"
        
        return summary
    
    def _generate_comparison_analysis(self, properties_data, location, query):
        """Compare locations or property types"""
        summary = f"**Comparison Analysis**\n\n"
        
        by_location = defaultdict(list)
        for prop in properties_data:
            by_location[prop.get('location')].append(prop)
        
        summary += "**By Location:**\n"
        for loc, props in sorted(by_location.items()):
            prices = [float(p.get('price', 0)) for p in props if p.get('price')]
            demands = [float(p.get('demand_score', 0)) for p in props if p.get('demand_score')]
            
            summary += f"\n**{loc}**\n"
            summary += f"- Properties: {len(props)}\n"
            summary += f"- Avg Price: ${sum(prices)/len(prices):,.0f}\n"
            summary += f"- Price Range: ${min(prices):,.0f} - ${max(prices):,.0f}\n"
            summary += f"- Avg Demand: {sum(demands)/len(demands):.0f}\n"
            summary += f"- High Demand: {sum(1 for d in demands if d > 2000)} properties\n"
        
        return summary
    
    def _generate_trend_analysis(self, properties_data, location, query):
        """Analyze price and demand trends over years"""
        summary = f"**Market Trends Analysis**\n\n"
        
        by_year = defaultdict(list)
        for prop in properties_data:
            by_year[prop.get('year', 0)].append(prop)
        
        summary += "**Price Trends by Year:**\n"
        for year in sorted(by_year.keys()):
            props = by_year[year]
            prices = [float(p.get('price', 0)) for p in props if p.get('price')]
            demands = [float(p.get('demand_score', 0)) for p in props if p.get('demand_score')]
            
            summary += f"\n{year}:\n"
            summary += f"- {len(props)} properties\n"
            summary += f"- Avg Price: ${sum(prices)/len(prices):,.0f}\n"
            summary += f"- Avg Demand: {sum(demands)/len(demands):.0f}\n"
        
        # Add trend insight
        sorted_years = sorted(by_year.keys())
        if len(sorted_years) > 1:
            first_year_price = sum(float(p.get('price', 0)) for p in by_year[sorted_years[0]]) / len(by_year[sorted_years[0]])
            last_year_price = sum(float(p.get('price', 0)) for p in by_year[sorted_years[-1]]) / len(by_year[sorted_years[-1]])
            change = ((last_year_price - first_year_price) / first_year_price * 100) if first_year_price else 0
            
            summary += f"\n**Price Trend:** {change:+.1f}% from {sorted_years[0]} to {sorted_years[-1]}\n"
        
        return summary
    
    def _generate_recommendations(self, properties_data, location, query):
        """Generate investment recommendations"""
        summary = f"**Investment Recommendations**\n\n"
        
        prices = [float(p.get('price', 0)) for p in properties_data if p.get('price')]
        demands = [float(p.get('demand_score', 0)) for p in properties_data if p.get('demand_score')]
        
        avg_price = sum(prices) / len(prices) if prices else 0
        avg_demand = sum(demands) / len(demands) if demands else 0
        
        # Sort properties by value (low price + high demand)
        value_score = []
        for prop in properties_data:
            price = float(prop.get('price', 0))
            demand = float(prop.get('demand_score', 0))
            # Value = high demand + low price
            score = (demand / avg_demand) - (price / avg_price)
            value_score.append((prop, score))
        
        value_score.sort(key=lambda x: x[1], reverse=True)
        
        summary += "**Top Value Picks** (High Demand + Affordable):\n"
        for prop, score in value_score[:5]:
            summary += f"- {prop.get('location')} | ${prop.get('price', 0):,.0f} | Demand: {prop.get('demand_score', 0):.0f}\n"
        
        summary += "\n**Premium Segment** (High Price + High Demand):\n"
        premium = [p for p in value_score if float(p[0].get('price', 0)) > avg_price and float(p[0].get('demand_score', 0)) > avg_demand]
        for prop, score in premium[:3]:
            summary += f"- {prop.get('location')} | ${prop.get('price', 0):,.0f} | Demand: {prop.get('demand_score', 0):.0f}\n"
        
        summary += "\n**Budget Options** (Low Price):\n"
        budget = sorted(value_score, key=lambda x: float(x[0].get('price', 0)))[:3]
        for prop, score in budget:
            summary += f"- {prop.get('location')} | ${prop.get('price', 0):,.0f} | Demand: {prop.get('demand_score', 0):.0f}\n"
        
        return summary
    
    def _generate_general_analysis(self, properties_data, location, query):
        """Default general analysis"""
        return self._format_property_listing(properties_data, location)


class QueryClassifier:
    """Classify user queries to determine how to handle them"""
    
    @staticmethod
    def classify(query_text):
        """Classify query type and extract intent"""
        query_lower = query_text.lower()
        
        # Listing queries
        if any(word in query_lower for word in ['list', 'show', 'all properties', 'tell me about', 'details']):
            return 'listing'
        
        # Comparison queries
        if any(word in query_lower for word in ['compare', 'comparison', 'vs', 'versus', 'better', 'which']):
            return 'comparison'
        
        # Trend queries
        if any(word in query_lower for word in ['trend', 'growth', 'increase', 'decrease', 'over time', 'year', 'historical']):
            return 'trend'
        
        # Recommendation queries
        if any(word in query_lower for word in ['recommend', 'best', 'invest', 'buy', 'good investment', 'value']):
            return 'recommendation'
        
        # Price queries
        if any(word in query_lower for word in ['price', 'cost', 'afford', 'expensive']):
            return 'comparison'
        
        # Demand queries
        if any(word in query_lower for word in ['demand', 'popular', 'interested', 'sales']):
            return 'trend'
        
        return 'general'
        """Generate natural language summary using Gemini"""
        try:
            if not properties_data:
                return "No data available for the given query."
            
            # Build detailed summary from actual property data
            summary = f"**Properties in {location or 'Database'}**\n\n"
            summary += f"Total Properties: {len(properties_data)}\n\n"
            
            # Group by property type
            from collections import defaultdict
            by_type = defaultdict(list)
            for prop in properties_data:
                by_type[prop.get('property_type', 'Unknown')].append(prop)
            
            # Show properties by type
            for ptype, props in by_type.items():
                summary += f"**{ptype.title()}** ({len(props)} properties):\n"
                for prop in props:
                    summary += f"- Year {prop.get('year')}: ${prop.get('price', 0):,.2f} | Demand: {prop.get('demand_score', 0):.0f}\n"
                summary += "\n"
            
            # Add statistics
            prices = [float(p.get('price', 0)) for p in properties_data if p.get('price')]
            demands = [float(p.get('demand_score', 0)) for p in properties_data if p.get('demand_score')]
            
            if prices:
                summary += f"**Statistics:**\n"
                summary += f"- Average Price: ${sum(prices)/len(prices):,.2f}\n"
                summary += f"- Price Range: ${min(prices):,.2f} - ${max(prices):,.2f}\n"
                summary += f"- Average Demand Score: {sum(demands)/len(demands):.0f}\n"
            
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"


class DataProcessingService:
    @staticmethod
    def parse_query(query_text):
        """Parse user query to extract location and analysis type"""
        query_lower = query_text.lower()
        
        # Common locations to check
        locations = [
            'wakad', 'pune', 'bengaluru', 'bangalore', 'mumbai', 'delhi',
            'gurgaon', 'noida', 'hyderabad', 'kolkata', 'ahmedabad', 'jaipur'
        ]
        
        extracted_location = None
        for loc in locations:
            if loc in query_lower:
                extracted_location = loc.capitalize()
                break
        
        return {
            'location': extracted_location,
            'query': query_text
        }
    
    @staticmethod
    def filter_properties(location=None, property_type=None, year_range=None):
        """Filter properties based on criteria"""
        queryset = Property.objects.all()
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        if year_range and len(year_range) == 2:
            queryset = queryset.filter(year__range=year_range)
        
        return queryset
    
    @staticmethod
    def prepare_chart_data(properties):
        """Prepare data for chart visualization"""
        data_by_year = {}
        
        for prop in properties:
            year = prop.year
            if year not in data_by_year:
                data_by_year[year] = {
                    'year': year,
                    'avgPrice': 0,
                    'avgDemand': 0,
                    'count': 0,
                }
            
            data_by_year[year]['avgPrice'] += float(prop.price)
            data_by_year[year]['avgDemand'] += float(prop.demand_score)
            data_by_year[year]['count'] += 1
        
        # Calculate averages
        for year in data_by_year:
            count = data_by_year[year]['count']
            data_by_year[year]['avgPrice'] = round(data_by_year[year]['avgPrice'] / count, 2)
            data_by_year[year]['avgDemand'] = round(data_by_year[year]['avgDemand'] / count, 2)
            del data_by_year[year]['count']
        
        return sorted(data_by_year.values(), key=lambda x: x['year'])
    
    @staticmethod
    def prepare_table_data(properties):
        """Prepare data for table display"""
        table_data = []
        for prop in properties:
            table_data.append({
                'location': prop.location,
                'type': prop.property_type,
                'price': float(prop.price),
                'pricePerSqft': float(prop.price_per_sqft) if prop.price_per_sqft else None,
                'area': float(prop.area_sqft) if prop.area_sqft else None,
                'year': prop.year,
                'demand': prop.demand,
                'demandScore': float(prop.demand_score),
            })
        return table_data
