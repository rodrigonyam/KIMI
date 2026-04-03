# Advanced Analysis - Customer Behavior & Business Insights

print("=" * 70)
print("ADVANCED BUSINESS INSIGHTS")
print("=" * 70)

# 1. RFM-like Analysis (using transaction frequency)
print("\n📊 TRANSACTION FREQUENCY ANALYSIS")
print("-" * 50)
transaction_stats = df.groupby('transaction_id').agg({
    'total_amount': 'sum',
    'quantity': 'sum',
    'date': 'first'
}).reset_index()

print(f"Average Transaction Value: ${transaction_stats['total_amount'].mean():.2f}")
print(f"Median Transaction Value: ${transaction_stats['total_amount'].median():.2f}")
print(f"Average Items per Transaction: {transaction_stats['quantity'].mean():.1f}")

# Transaction value distribution
bins = [0, 10, 25, 50, 100, float('inf')]
labels = ['$0-10', '$10-25', '$25-50', '$50-100', '$100+']
transaction_stats['value_segment'] = pd.cut(transaction_stats['total_amount'], bins=bins, labels=labels)
print(f"\nTransaction Value Segments:")
print(transaction_stats['value_segment'].value_counts().sort_index())

# 2. Category Performance Metrics
print("\n\n📈 CATEGORY PERFORMANCE METRICS")
print("-" * 50)
category_metrics = df.groupby('category').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'unit_price': 'mean'
}).round(2)
category_metrics.columns = ['Total Revenue', 'Avg Transaction', 'Transaction Count', 'Units Sold', 'Avg Unit Price']
category_metrics['Revenue per Unit'] = (category_metrics['Total Revenue'] / category_metrics['Units Sold']).round(2)
category_metrics = category_metrics.sort_values('Total Revenue', ascending=False)
print(category_metrics)

# 3. Seasonal Analysis
print("\n\n🗓️ SEASONAL PATTERNS")
print("-" * 50)
seasonal = df.groupby('month').agg({
    'total_amount': 'sum',
    'transaction_id': 'nunique'
}).round(2)
seasonal.columns = ['Total Sales', 'Unique Transactions']

# Add season mapping
month_to_season = {
    'January': 'Winter', 'February': 'Winter', 'March': 'Spring',
    'April': 'Spring', 'May': 'Spring', 'June': 'Summer',
    'July': 'Summer', 'August': 'Summer', 'September': 'Fall',
    'October': 'Fall', 'November': 'Fall', 'December': 'Winter'
}
seasonal['Season'] = seasonal.index.map(month_to_season)
print(seasonal)

print(f"\nBy Season:")
season_summary = seasonal.groupby('Season')['Total Sales'].sum().sort_values(ascending=False)
for season, sales in season_summary.items():
    pct = (sales / seasonal['Total Sales'].sum()) * 100
    print(f"  {season}: ${sales:,.2f} ({pct:.1f}%)")

# 4. Weekend vs Weekday Analysis
print("\n\n📅 WEEKEND VS WEEKDAY ANALYSIS")
print("-" * 50)
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
weekend_analysis = df.groupby('is_weekend').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'transaction_id': 'nunique'
}).round(2)
weekend_analysis.index = ['Weekday', 'Weekend']
weekend_analysis.columns = ['Total Sales', 'Avg Sale', 'Item Count', 'Transactions']
print(weekend_analysis)

# 5. Top Performing Products Deep Dive
print("\n\n🏆 TOP 5 PRODUCTS BY REVENUE")
print("-" * 50)
top_products = df.groupby(['category', 'product']).agg({
    'total_amount': 'sum',
    'quantity': 'sum',
    'transaction_id': 'nunique'
}).round(2)
top_products.columns = ['Revenue', 'Units Sold', 'Transactions']
top_products['Avg Price'] = (top_products['Revenue'] / top_products['Units Sold']).round(2)
top_products = top_products.sort_values('Revenue', ascending=False).head(5)
print(top_products)

# 6. Price Sensitivity Analysis
print("\n\n💰 PRICE SENSITIVITY INSIGHTS")
print("-" * 50)
price_ranges = pd.cut(df['unit_price'], bins=[0, 5, 10, 20, 50, float('inf')], 
                      labels=['$0-5', '$5-10', '$10-20', '$20-50', '$50+'])
price_analysis = df.groupby(price_ranges).agg({
    'quantity': 'sum',
    'total_amount': 'sum',
    'transaction_id': 'count'
}).round(2)
price_analysis.columns = ['Units Sold', 'Revenue', 'Transactions']
price_analysis['Avg Qty per Transaction'] = (price_analysis['Units Sold'] / price_analysis['Transactions']).round(2)
print(price_analysis)
