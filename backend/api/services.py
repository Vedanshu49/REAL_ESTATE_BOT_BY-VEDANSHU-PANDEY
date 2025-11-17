import google.generativeai as genai
from django.conf import settings
import json
from django.db.models import Avg, Count, Sum, Q
from .models import Property
from collections import defaultdict
import statistics
from decimal import Decimal
from datetime import datetime, date


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal and datetime objects"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return str(obj)
        return super().default(obj)


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_intelligent_summary(self, properties_data, location=None, query=None, query_type=None):
        """Generate TRULY intelligent conversational summaries using Gemini AI"""
        try:
            if not properties_data:
                return "No data available for the given query."
            
            # Convert properties_data to JSON-serializable format
            properties_data = self._ensure_json_serializable(properties_data)
            
            # Prepare rich data context for Gemini
            data_context = self._prepare_data_context(properties_data, location, query_type)
            
            # Build a smart prompt that uses Gemini's full conversational power
            prompt = self._build_intelligent_prompt(query, properties_data, data_context, query_type, location)
            
            # Call Gemini with streaming for real-time response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,  # Creative but factual
                    top_p=0.95,
                    top_k=50,
                    max_output_tokens=3000
                ),
                safety_settings=[
                    {
                        "category": genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
                    },
                    {
                        "category": genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
                    },
                    {
                        "category": genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
                    },
                    {
                        "category": genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
                    }
                ]
            )
            
            summary = response.text if response and response.text else "Unable to generate analysis."
            # Don't fall back to generic response - if there's an issue, it will be clear
            return summary
        
        except Exception as e:
            print(f"Gemini Error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return more informative error
            return f"Error generating analysis: {str(e)}"
    
    def _ensure_json_serializable(self, properties_data):
        """Convert all properties to JSON-serializable format"""
        serializable_data = []
        for prop in properties_data:
            clean_prop = {}
            for key, value in prop.items():
                if isinstance(value, Decimal):
                    clean_prop[key] = float(value)
                elif isinstance(value, (datetime, date)):
                    clean_prop[key] = str(value)
                else:
                    clean_prop[key] = value
            serializable_data.append(clean_prop)
        return serializable_data
    
    def _prepare_data_context(self, properties_data, location, query_type):
        """Prepare rich, analytical data context for Gemini to analyze"""
        context = {
            'total_properties': len(properties_data),
            'locations': list(set(p.get('location') for p in properties_data)),
            'price_stats': self._calculate_price_stats(properties_data),
            'demand_stats': self._calculate_demand_stats(properties_data),
            'property_types': self._categorize_by_type(properties_data),
            'year_analysis': self._analyze_by_year(properties_data),
            'location_comparison': self._compare_locations(properties_data),
            'investment_insights': self._calculate_investment_metrics(properties_data),
            'market_trends': self._identify_trends(properties_data),
            'top_properties': self._identify_top_properties(properties_data)
        }
        return context
    
    def _calculate_price_stats(self, properties_data):
        """Calculate comprehensive price statistics"""
        prices = [float(p.get('price', 0)) for p in properties_data if p.get('price')]
        if not prices:
            return {}
        
        return {
            'min': min(prices),
            'max': max(prices),
            'avg': sum(prices) / len(prices),
            'median': statistics.median(prices),
            'std_dev': statistics.stdev(prices) if len(prices) > 1 else 0
        }
    
    def _calculate_demand_stats(self, properties_data):
        """Calculate comprehensive demand statistics"""
        demands = [float(p.get('demand_score', 0)) for p in properties_data if p.get('demand_score')]
        if not demands:
            return {}
        
        return {
            'min': min(demands),
            'max': max(demands),
            'avg': sum(demands) / len(demands),
            'median': statistics.median(demands),
            'high_demand': sum(1 for d in demands if d > statistics.median(demands) * 1.2)
        }
    
    def _categorize_by_type(self, properties_data):
        """Categorize properties by type with insights"""
        by_type = defaultdict(list)
        for prop in properties_data:
            by_type[prop.get('property_type', 'Residential')].append(prop)
        
        result = {}
        for ptype, props in by_type.items():
            prices = [float(p.get('price', 0)) for p in props if p.get('price')]
            result[ptype] = {
                'count': len(props),
                'avg_price': sum(prices) / len(prices) if prices else 0,
                'price_range': [min(prices), max(prices)] if prices else [0, 0]
            }
        return result
    
    def _analyze_by_year(self, properties_data):
        """Analyze properties by year - important for trends"""
        by_year = defaultdict(list)
        for prop in properties_data:
            by_year[prop.get('year', 0)].append(prop)
        
        result = {}
        for year in sorted(by_year.keys()):
            props = by_year[year]
            prices = [float(p.get('price', 0)) for p in props if p.get('price')]
            demands = [float(p.get('demand_score', 0)) for p in props if p.get('demand_score')]
            
            result[year] = {
                'count': len(props),
                'avg_price': sum(prices) / len(prices) if prices else 0,
                'avg_demand': sum(demands) / len(demands) if demands else 0
            }
        return result
    
    def _compare_locations(self, properties_data):
        """Compare locations for market insights"""
        by_location = defaultdict(list)
        for prop in properties_data:
            by_location[prop.get('location')].append(prop)
        
        result = {}
        for loc, props in by_location.items():
            prices = [float(p.get('price', 0)) for p in props if p.get('price')]
            demands = [float(p.get('demand_score', 0)) for p in props if p.get('demand_score')]
            
            result[loc] = {
                'count': len(props),
                'avg_price': sum(prices) / len(prices) if prices else 0,
                'min_price': min(prices) if prices else 0,
                'max_price': max(prices) if prices else 0,
                'price_range': [min(prices), max(prices)] if prices else [0, 0],
                'avg_demand': sum(demands) / len(demands) if demands else 0,
                'high_demand_count': sum(1 for d in demands if d > 2000)
            }
        return result
    
    def _calculate_investment_metrics(self, properties_data):
        """Calculate ROI and investment potential metrics"""
        metrics = []
        for prop in properties_data:
            price = float(prop.get('price', 0))
            demand = float(prop.get('demand_score', 0))
            
            if price > 0:
                roi_score = (demand / price) * 100000  # Normalized score
                metrics.append({
                    'location': prop.get('location'),
                    'price': price,
                    'demand': demand,
                    'roi_score': roi_score,
                    'investment_rating': 'Excellent' if roi_score > 80 else 'Good' if roi_score > 50 else 'Fair'
                })
        
        return sorted(metrics, key=lambda x: x['roi_score'], reverse=True)[:5]
    
    def _identify_trends(self, properties_data):
        """Identify market trends from year-over-year data"""
        by_year = defaultdict(list)
        for prop in properties_data:
            by_year[prop.get('year', 0)].append(prop)
        
        trends = []
        years = sorted(by_year.keys())
        
        for i in range(len(years) - 1):
            year1, year2 = years[i], years[i + 1]
            props1 = by_year[year1]
            props2 = by_year[year2]
            
            prices1 = [float(p.get('price', 0)) for p in props1 if p.get('price')]
            prices2 = [float(p.get('price', 0)) for p in props2 if p.get('price')]
            
            if prices1 and prices2:
                avg1 = sum(prices1) / len(prices1)
                avg2 = sum(prices2) / len(prices2)
                change = ((avg2 - avg1) / avg1) * 100
                
                trends.append({
                    'period': f"{year1} to {year2}",
                    'change_percent': change,
                    'direction': 'UP' if change > 0 else 'DOWN'
                })
        
        return trends
    
    def _identify_top_properties(self, properties_data):
        """Identify top performing properties"""
        ranked = []
        for prop in properties_data:
            score = (float(prop.get('demand_score', 0)) * 0.6) - (float(prop.get('price', 0)) / 100000 * 0.4)
            ranked.append({**prop, 'investment_score': score})
        
        return sorted(ranked, key=lambda x: x['investment_score'], reverse=True)[:5]
    
    def _build_intelligent_prompt(self, user_query, properties_data, data_context, query_type, location):
        """Build a smart prompt that gets the best out of Gemini"""
        
        # Create a comprehensive data summary for context
        locations_list = data_context['locations']
        
        # Build location-specific insights
        location_insights = ""
        for loc, stats in data_context['location_comparison'].items():
            location_insights += f"\n{loc}: {stats['count']} properties, Avg ${stats['avg_price']:,.0f}, Demand {stats['avg_demand']:.0f}"
        
        # Build investment top picks
        investment_picks = ""
        for inv in data_context['investment_insights'][:5]:
            investment_picks += f"\n- {inv['location']}: Price ${inv['price']:,.0f}, Demand {inv['demand']:.0f}, ROI Score {inv['roi_score']:.2f}"
        
        # Build trend insights
        trend_insights = ""
        for trend in data_context['market_trends']:
            trend_insights += f"\n- {trend['period']}: {trend['direction']} {abs(trend['change_percent']):.1f}%"
        
        # Get top 3 highest demand properties with details
        top_demand_props = sorted(
            [p for p in properties_data],
            key=lambda x: float(x.get('demand_score', 0)),
            reverse=True
        )[:3]
        
        top_demand_str = ""
        for i, prop in enumerate(top_demand_props, 1):
            top_demand_str += f"\n{i}. {prop.get('location')} - Demand: {float(prop.get('demand_score', 0)):.0f}, Price: ${float(prop.get('price', 0)):,.0f}, Type: {prop.get('property_type')}"
        
        # Get unique areas with their average metrics
        areas_summary = ""
        for loc, stats in data_context['location_comparison'].items():
            areas_summary += f"\n• {loc}: {stats['count']} properties | Avg Price: ${stats['avg_price']:,.0f} | Avg Demand: {stats['avg_demand']:.0f} | Price Range: ${stats['min_price']:,.0f}-${stats['max_price']:,.0f}"
        
        # Create property database list
        property_db = []
        for p in properties_data:
            property_db.append({
                'location': p.get('location'),
                'type': p.get('property_type'),
                'price': float(p.get('price', 0)),
                'demand_score': float(p.get('demand_score', 0)),
                'year': p.get('year')
            })
        
        property_db_json = json.dumps(property_db, indent=2, cls=DecimalEncoder)
        
        # Create high performing properties list
        high_performing = []
        for p in properties_data:
            if p.get('demand_score', 0) > data_context['demand_stats'].get('avg', 0):
                high_performing.append({
                    'location': p.get('location'),
                    'type': p.get('property_type'),
                    'price': float(p.get('price', 0)),
                    'demand_score': float(p.get('demand_score', 0)),
                    'year': p.get('year')
                })
        
        high_performing_json = json.dumps(high_performing, indent=2, cls=DecimalEncoder)
        
        prompt = f"""You are a WORLD-CLASS real estate market analyst and investment advisor.
You MUST provide SPECIFIC, DATA-DRIVEN answers that directly address the user's question.

USER QUERY: "{user_query}"

RESPONSE GUIDELINES:
✓ DIRECTLY answer what was asked - don't give generic market summaries
✓ CITE SPECIFIC properties, locations, and numbers
✓ Sound like an expert advisor giving personalized insights
✓ When asked "What's the highest demand property?" - TELL THEM THE NAME, DEMAND SCORE, and PRICE
✓ When asked "list all areas" - Give EACH area with metrics, not just names
✓ When asked for "trends" - Explain what's happening and WHY
✓ NEVER respond with just "Analysis of X properties - Average Price: $Y"
✓ Make every response valuable and specific to THEIR question
✓ Use comparisons and insights to help them understand the market

MARKET DATA CONTEXT:

MARKET OVERVIEW:
- Total Properties: {data_context['total_properties']}
- All Locations: {', '.join(locations_list)}
- Price Range: ${data_context['price_stats'].get('min', 0):,.0f} - ${data_context['price_stats'].get('max', 0):,.0f}
- Average Price: ${data_context['price_stats'].get('avg', 0):,.0f}
- Median Price: ${data_context['price_stats'].get('median', 0):,.0f}

DEMAND ANALYSIS:
- Average Market Demand: {data_context['demand_stats'].get('avg', 0):.0f}
- Highest Demand Score: {data_context['demand_stats'].get('max', 0):.0f}
- Top 3 Highest Demand Properties:{top_demand_str}

AREAS & LOCATIONS:
{areas_summary}

PROPERTY TYPE BREAKDOWN:
{json.dumps(data_context['property_types'], indent=2, cls=DecimalEncoder)}

TOP INVESTMENT OPPORTUNITIES:
{investment_picks}

MARKET TRENDS:
{trend_insights}

HIGH-PERFORMING PROPERTIES (Above Average Demand):
{high_performing_json}

COMPLETE PROPERTY DATABASE:
{property_db_json}

Remember: Answer the SPECIFIC question asked with SPECIFIC data. No generic responses."""
        return prompt
    
    def _calc_avg_price(self, properties_data):
        """Helper to calculate average price"""
        prices = [float(p.get('price', 0)) for p in properties_data if p.get('price')]
        return sum(prices) / len(prices) if prices else 0
    
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
