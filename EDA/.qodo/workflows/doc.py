# I'll create a comprehensive EDA project for a mid-level retail store
# This will include data generation, analysis, and visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Define product categories and items
categories = {
    'Vitamins & Supplements': ['Multivitamin', 'Vitamin C', 'Vitamin D', 'Fish Oil', 'Probiotics', 'Calcium', 'Iron', 'B-Complex', 'Magnesium', 'Zinc'],
    'Energy Drinks': ['Red Bull', 'Monster', 'Rockstar', 'Celsius', 'Bang', '5-Hour Energy', 'Gatorade', 'Powerade', 'NOS', 'Reign'],
    'Cleaning Supplies': ['All-Purpose Cleaner', 'Disinfectant Wipes', 'Glass Cleaner', 'Floor Cleaner', 'Laundry Detergent', 'Dish Soap', 'Bleach', 'Air Freshener', 'Toilet Bowl Cleaner', 'Sponges'],
    'Personal Care': ['Shampoo', 'Conditioner', 'Body Wash', 'Toothpaste', 'Deodorant', 'Hand Soap', 'Facial Cleanser', 'Lotion', 'Sunscreen', 'Mouthwash'],
    'Health & Wellness': ['First Aid Kit', 'Pain Relievers', 'Cough Syrup', 'Bandages', 'Thermometer', 'Blood Pressure Monitor', 'Heating Pad', 'Ice Pack', 'Antacids', 'Allergy Meds']
}

# Generate synthetic data
n_transactions = 15000
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

# Create date range
dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_transactions)]
dates.sort()

# Generate transaction data
transactions = []
transaction_id = 1000

for date in dates:
    # Determine number of items in this transaction (1-5 items)
    n_items = np.random.randint(1, 6)
    
    for _ in range(n_items):
        category = np.random.choice(list(categories.keys()))
        product = np.random.choice(categories[category])
        
        # Pricing based on category
        if category == 'Vitamins & Supplements':
            price = np.random.uniform(8, 35)
        elif category == 'Energy Drinks':
            price = np.random.uniform(2, 6)
        elif category == 'Cleaning Supplies':
            price = np.random.uniform(3, 15)
        elif category == 'Personal Care':
            price = np.random.uniform(4, 20)
        else:  # Health & Wellness
            price = np.random.uniform(5, 45)
        
        quantity = np.random.randint(1, 4)
        
        # Seasonal effects
        month = date.month
        if category == 'Energy Drinks' and month in [6, 7, 8]:  # Summer boost
            quantity = min(quantity + 1, 5)
        if category == 'Vitamins & Supplements' and month in [1, 2]:  # New Year resolutions
            quantity = min(quantity + 1, 5)
        if category == 'Cleaning Supplies' and month in [3, 4]:  # Spring cleaning
            quantity = min(quantity + 1, 5)
        
        # Weekend vs weekday effect
        is_weekend = date.weekday() >= 5
        if is_weekend:
            quantity = min(quantity + np.random.randint(0, 2), 5)
        
        transactions.append({
            'transaction_id': f'TXN-{transaction_id}',
            'date': date,
            'category': category,
            'product': product,
            'quantity': quantity,
            'unit_price': round(price, 2),
            'total_amount': round(price * quantity, 2),
            'day_of_week': date.strftime('%A'),
            'month': date.strftime('%B'),
            'quarter': f'Q{(date.month-1)//3 + 1}'
        })
    
    transaction_id += 1

# Create DataFrame
df = pd.DataFrame(transactions)

print("=" * 60)
print("RETAIL STORE DATA OVERVIEW")
print("=" * 60)
print(f"\nDataset Shape: {df.shape}")
print(f"Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
print(f"\nColumn Names:\n{df.columns.tolist()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nDuplicated Rows: {df.duplicated().sum()}")

# Display sample data
print("\n" + "=" * 60)
print("SAMPLE DATA (First 10 rows)")
print("=" * 60)
print(df.head(10).to_string())
