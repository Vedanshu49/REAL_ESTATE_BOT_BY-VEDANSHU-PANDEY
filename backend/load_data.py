import os
import django
import pandas as pd
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Property


def load_excel_data(excel_path):
    """Load data from Excel file and populate the database"""
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)
        
        print(f"Loading data from {excel_path}...")
        print(f"Found {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
        # Clear existing data
        Property.objects.all().delete()
        print("Cleared existing properties")
        
        # Prepare batch insert
        properties = []
        
        for idx, row in df.iterrows():
            try:
                # Map Excel columns to model fields (handle various column names)
                location = row.get('final location') or row.get('Location') or 'Unknown'
                year = int(row.get('year', 2024)) if pd.notna(row.get('year')) else 2024
                
                # Get price - try multiple column names
                price = 0
                for col in ['flat - weighted average rate', 'Price', 'price']:
                    if col in row and pd.notna(row[col]):
                        try:
                            price = float(row[col])
                            break
                        except:
                            pass
                
                # Get demand data
                total_sales = int(row.get('total_sales - igr', 0)) if pd.notna(row.get('total_sales - igr')) else 0
                demand_score = float(row.get('total sold - igr', 0)) if pd.notna(row.get('total sold - igr')) else 0.0
                
                # Get area
                area_sqft = None
                for col in ['total carpet area supplied (sqft)', 'Area', 'area_sqft']:
                    if col in row and pd.notna(row[col]):
                        try:
                            area_sqft = float(row[col])
                            break
                        except:
                            pass
                
                # Calculate price per sqft
                price_per_sqft = None
                if area_sqft and area_sqft > 0 and price > 0:
                    price_per_sqft = price / (area_sqft / 1000)  # Assuming area is in sqft
                
                prop = Property(
                    location=str(location).strip(),
                    property_type='residential',  # Default type
                    price=price,
                    price_per_sqft=price_per_sqft,
                    area_sqft=area_sqft,
                    year=year,
                    demand=total_sales,
                    demand_score=demand_score,
                )
                properties.append(prop)
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue
        
        # Bulk create
        Property.objects.bulk_create(properties, batch_size=100)
        print(f"Successfully loaded {len(properties)} properties into database")
        
        # Print summary
        locations = Property.objects.values_list('location', flat=True).distinct()
        print(f"Locations: {list(locations)}")
        print(f"Total properties: {Property.objects.count()}")
        
    except Exception as e:
        print(f"Error loading data: {e}")


if __name__ == '__main__':
    # Find Sample_data.xlsx in parent directory
    project_root = Path(__file__).resolve().parent.parent
    excel_file = project_root / 'Sample_data.xlsx'
    
    if excel_file.exists():
        load_excel_data(str(excel_file))
    else:
        print(f"Excel file not found at {excel_file}")
        print(f"Please place Sample_data.xlsx in the project root directory")
