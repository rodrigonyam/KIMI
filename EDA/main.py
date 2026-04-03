# Retail Store EDA - Consolidated Analysis Script
# Covers: data generation, descriptive stats, business insights,
#         comprehensive visualizations, and advanced analysis.

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# =============================================================
# 1. DATA GENERATION
# =============================================================

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

n_transactions = 15000

# Customer pool: 2000 unique customers, top 20% are heavy buyers (5x visit rate)
N_CUSTOMERS = 2000
customer_ids = [f'C{str(i).zfill(4)}' for i in range(1, N_CUSTOMERS + 1)]
customer_weights = np.concatenate([
    np.full(int(N_CUSTOMERS * 0.2), 5.0),
    np.full(N_CUSTOMERS - int(N_CUSTOMERS * 0.2), 1.0)
])
customer_weights /= customer_weights.sum()

start_date = datetime(2025, 1, 1)

# Create date range
dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_transactions)]
dates.sort()

# Generate transaction data
transactions = []
transaction_id = 1000

for date in dates:
    # Assign one customer per transaction (heavy buyers sampled more often)
    cust_id = np.random.choice(customer_ids, p=customer_weights)
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
        if category == 'Energy Drinks' and month in [6, 7, 8]:       # Summer boost
            quantity = min(quantity + 1, 5)
        if category == 'Vitamins & Supplements' and month in [1, 2]: # New Year resolutions
            quantity = min(quantity + 1, 5)
        if category == 'Cleaning Supplies' and month in [3, 4]:      # Spring cleaning
            quantity = min(quantity + 1, 5)

        # Weekend vs weekday effect
        is_weekend = date.weekday() >= 5
        if is_weekend:
            quantity = min(quantity + np.random.randint(0, 2), 5)

        transactions.append({
            'transaction_id': f'TXN-{transaction_id}',
            'customer_id': cust_id,
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

# Create DataFrame and derive is_weekend once
df = pd.DataFrame(transactions)
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])

# =============================================================
# 2. DATA OVERVIEW
# =============================================================

print("=" * 60)
print("RETAIL STORE DATA OVERVIEW")
print("=" * 60)
print(f"\nDataset Shape: {df.shape}")
print(f"Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
print(f"\nColumn Names:\n{df.columns.tolist()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nDuplicated Rows: {df.duplicated().sum()}")

print("\n" + "=" * 60)
print("SAMPLE DATA (First 10 rows)")
print("=" * 60)
print(df.head(10).to_string())

# =============================================================
# 3. DESCRIPTIVE STATISTICS
# =============================================================

print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

print("\nNUMERIC COLUMNS SUMMARY:")
print(df[['quantity', 'unit_price', 'total_amount']].describe().round(2))

print("\n" + "-" * 60)
print("CATEGORICAL COLUMNS - TOP VALUES:")
print("-" * 60)

print(f"\nTop 10 Products by Frequency:")
print(df['product'].value_counts().head(10))

print(f"\nCategory Distribution:")
print(df['category'].value_counts())

print(f"\nQuarterly Distribution:")
print(df['quarter'].value_counts().sort_index())

print(f"\nDay of Week Distribution:")
print(df['day_of_week'].value_counts())

# =============================================================
# 4. ADVANCED BUSINESS INSIGHTS
# =============================================================

print("\n" + "=" * 70)
print("ADVANCED BUSINESS INSIGHTS")
print("=" * 70)

# 1. Customer Overview
print("\n👥 CUSTOMER OVERVIEW")
print("-" * 50)
print(f"Unique Customers:         {df['customer_id'].nunique()}")
print(f"Unique Transactions:      {df['transaction_id'].nunique()}")
txn_per_cust = df.groupby('customer_id')['transaction_id'].nunique()
print(f"Avg Visits per Customer:  {txn_per_cust.mean():.1f}")
print(f"Median Visits:            {txn_per_cust.median():.0f}")
repeat_rate = (txn_per_cust > 1).mean() * 100
print(f"Repeat Purchase Rate:     {repeat_rate:.1f}%")

# 2. RFM Analysis
print("\n\n📊 RFM ANALYSIS (Recency / Frequency / Monetary)")
print("-" * 50)
reference_date = datetime(2026, 1, 1)

rfm = df.groupby('customer_id').agg(
    Recency=('date', lambda x: (reference_date - x.max()).days),
    Frequency=('transaction_id', 'nunique'),
    Monetary=('total_amount', 'sum')
).reset_index()

# Score each dimension into quartiles (4 = best)
rfm['R_score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])          # lower recency days = more recent = better
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
rfm['M_score'] = pd.qcut(rfm['Monetary'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
rfm['RFM_total'] = rfm[['R_score', 'F_score', 'M_score']].astype(int).sum(axis=1)

def segment_customer(row):
    r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'
    elif r >= 3 and f == 2:
        return 'Potential Loyalists'
    elif r >= 3 and f == 1:
        return 'New Customers'
    elif r == 2 and f >= 3:
        return 'At Risk'
    elif r == 2 and f <= 2:
        return 'Needs Attention'
    elif r == 1 and f >= 3:
        return 'Cannot Lose Them'
    else:
        return 'Lost'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print(f"\nRFM Summary Statistics:")
print(rfm[['Recency', 'Frequency', 'Monetary']].describe().round(2))

print(f"\nCustomer Segments:")
seg_counts = rfm['Segment'].value_counts()
seg_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False)
seg_summary = pd.DataFrame({'Customers': seg_counts, 'Total Revenue': seg_revenue}).fillna(0)
seg_summary['Avg Revenue'] = (seg_summary['Total Revenue'] / seg_summary['Customers']).round(2)
seg_summary['% Customers'] = (seg_summary['Customers'] / len(rfm) * 100).round(1)
print(seg_summary.sort_values('Total Revenue', ascending=False))

transaction_stats = df.groupby('transaction_id').agg({
    'total_amount': 'sum',
    'quantity': 'sum',
    'date': 'first'
}).reset_index()
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

# =============================================================
# 5. COMPREHENSIVE VISUALIZATIONS (12-chart overview)
# =============================================================

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

fig = plt.figure(figsize=(20, 24))

# 1. Sales by Category (Pie Chart)
ax1 = fig.add_subplot(4, 3, 1)
category_sales = df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
colors = plt.cm.Set3(np.linspace(0, 1, len(category_sales)))
wedges, texts, autotexts = ax1.pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%',
                                    colors=colors, startangle=90)
ax1.set_title('Total Sales Distribution by Category', fontsize=14, fontweight='bold', pad=20)
plt.setp(autotexts, size=9, weight='bold')

# 2. Monthly Sales Trend
ax2 = fig.add_subplot(4, 3, 2)
monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()
ax2.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, markersize=6, color='#2E86AB')
ax2.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.3, color='#2E86AB')
ax2.set_title('Monthly Sales Trend (2025)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Sales ($)')
ax2.tick_params(axis='x', rotation=45)

# 3. Top 10 Products by Revenue
ax3 = fig.add_subplot(4, 3, 3)
product_revenue = df.groupby('product')['total_amount'].sum().sort_values(ascending=True).tail(10)
bars = ax3.barh(product_revenue.index, product_revenue.values, color='#A23B72')
ax3.set_title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
ax3.set_xlabel('Revenue ($)')
for bar in bars:
    width = bar.get_width()
    ax3.text(width + 50, bar.get_y() + bar.get_height()/2, f'${width:,.0f}',
             va='center', fontsize=9)

# 4. Sales by Day of Week
ax4 = fig.add_subplot(4, 3, 4)
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_sales = df.groupby('day_of_week')['total_amount'].sum().reindex(dow_order)
bars = ax4.bar(dow_sales.index, dow_sales.values,
               color=['#F18F01' if d in ['Saturday', 'Sunday'] else '#048A81' for d in dow_sales.index])
ax4.set_title('Sales by Day of Week', fontsize=14, fontweight='bold')
ax4.set_ylabel('Total Sales ($)')
ax4.tick_params(axis='x', rotation=45)
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 100, f'${height:,.0f}',
             ha='center', va='bottom', fontsize=9)

# 5. Category Performance Box Plot
ax5 = fig.add_subplot(4, 3, 5)
df.boxplot(column='total_amount', by='category', ax=ax5)
ax5.set_title('Transaction Amount Distribution by Category', fontsize=14, fontweight='bold')
ax5.set_xlabel('Category')
ax5.set_ylabel('Transaction Amount ($)')
fig.suptitle('')  # Remove automatic boxplot supertitle without affecting other figures
ax5.tick_params(axis='x', rotation=45)

# 6. Quantity Distribution
ax6 = fig.add_subplot(4, 3, 6)
quantity_dist = df['quantity'].value_counts().sort_index()
bars = ax6.bar(quantity_dist.index, quantity_dist.values, color='#6A4C93', edgecolor='white')
ax6.set_title('Quantity per Transaction Distribution', fontsize=14, fontweight='bold')
ax6.set_xlabel('Quantity')
ax6.set_ylabel('Frequency')
for bar in bars:
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height + 20, f'{int(height)}',
             ha='center', va='bottom', fontsize=10)

# 7. Quarterly Comparison
ax7 = fig.add_subplot(4, 3, 7)
quarterly_data = df.groupby('quarter').agg({
    'total_amount': 'sum',
    'transaction_id': 'nunique'
}).reset_index()
quarterly_data.columns = ['Quarter', 'Total Sales', 'Transactions']
x = np.arange(len(quarterly_data))
width = 0.35
ax7.bar(x - width/2, quarterly_data['Total Sales'], width, label='Total Sales', color='#F4A261')
ax7_twin = ax7.twinx()
ax7_twin.bar(x + width/2, quarterly_data['Transactions'], width, label='Transactions', color='#2A9D8F')
ax7.set_title('Quarterly Sales vs Transaction Count', fontsize=14, fontweight='bold')
ax7.set_xlabel('Quarter')
ax7.set_ylabel('Total Sales ($)', color='#F4A261')
ax7_twin.set_ylabel('Transaction Count', color='#2A9D8F')
ax7.set_xticks(x)
ax7.set_xticklabels(quarterly_data['Quarter'])
ax7.legend(loc='upper left')
ax7_twin.legend(loc='upper right')

# 8. Price Distribution by Category
ax8 = fig.add_subplot(4, 3, 8)
for category in df['category'].unique():
    data = df[df['category'] == category]['unit_price']
    ax8.hist(data, bins=20, alpha=0.6, label=category)
ax8.set_title('Unit Price Distribution by Category', fontsize=14, fontweight='bold')
ax8.set_xlabel('Unit Price ($)')
ax8.set_ylabel('Frequency')
ax8.legend(fontsize=8, loc='upper right')

# 9. Week-of-year × Day-of-week heatmap (full year, reveals weekly rhythms)
ax9 = fig.add_subplot(4, 3, 9)
df['week'] = df['date'].dt.isocalendar().week.astype(int)
df['dow_num'] = df['date'].dt.dayofweek          # 0=Mon … 6=Sun
pivot_weekly = (
    df.groupby(['dow_num', 'week'])['total_amount']
    .sum()
    .unstack(fill_value=0)
)
dow_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
pivot_weekly.index = dow_labels[:len(pivot_weekly)]
sns.heatmap(
    pivot_weekly,
    cmap='YlOrRd',
    ax=ax9,
    cbar_kws={'label': 'Sales ($)'},
    linewidths=0,
    xticklabels=4               # show every 4th week number to avoid crowding
)
ax9.set_title('Weekly Sales Rhythm (Full Year)', fontsize=14, fontweight='bold')
ax9.set_xlabel('Week of Year')
ax9.set_ylabel('Day of Week')

# 10. Category Market Share Over Time
ax10 = fig.add_subplot(4, 3, 10)
monthly_category = df.groupby([df['date'].dt.to_period('M'), 'category'])['total_amount'].sum().unstack(fill_value=0)
monthly_category_pct = monthly_category.div(monthly_category.sum(axis=1), axis=0) * 100
monthly_category_pct.plot(kind='area', stacked=True, ax=ax10, alpha=0.8)
ax10.set_title('Category Market Share Over Time (%)', fontsize=14, fontweight='bold')
ax10.set_xlabel('Month')
ax10.set_ylabel('Percentage (%)')
ax10.legend(loc='upper left', fontsize=8)
ax10.tick_params(axis='x', rotation=45)

# 11. Average Transaction Value by Category
ax11 = fig.add_subplot(4, 3, 11)
avg_transaction = df.groupby('category')['total_amount'].mean().sort_values(ascending=True)
bars = ax11.barh(avg_transaction.index, avg_transaction.values, color='#E76F51')
ax11.set_title('Average Transaction Value by Category', fontsize=14, fontweight='bold')
ax11.set_xlabel('Average Amount ($)')
for bar in bars:
    width = bar.get_width()
    ax11.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'${width:.2f}',
              va='center', fontsize=10)

# 12. Correlation Heatmap
ax12 = fig.add_subplot(4, 3, 12)
corr_data = df[['quantity', 'unit_price', 'total_amount']].corr()
sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, ax=ax12,
            square=True, fmt='.2f', cbar_kws={'label': 'Correlation'})
ax12.set_title('Correlation Matrix', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('output/retail_eda_overview.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("\n✅ Comprehensive EDA visualization saved to output/retail_eda_overview.png")

# =============================================================
# 6. ADVANCED ANALYSIS VISUALIZATIONS (6-chart)
# =============================================================

fig2 = plt.figure(figsize=(18, 14))

# 1. Transaction Value Distribution
ax1 = fig2.add_subplot(2, 3, 1)
transaction_totals = df.groupby('transaction_id')['total_amount'].sum()
ax1.hist(transaction_totals, bins=30, color='#264653', edgecolor='white', alpha=0.8)
ax1.axvline(transaction_totals.mean(), color='#E76F51', linestyle='--', linewidth=2,
            label=f'Mean: ${transaction_totals.mean():.2f}')
ax1.axvline(transaction_totals.median(), color='#2A9D8F', linestyle='--', linewidth=2,
            label=f'Median: ${transaction_totals.median():.2f}')
ax1.set_title('Distribution of Transaction Values', fontsize=14, fontweight='bold')
ax1.set_xlabel('Transaction Value ($)')
ax1.set_ylabel('Frequency')
ax1.legend()

# 2. Monthly Sales by Category (Stacked Bar)
ax2 = fig2.add_subplot(2, 3, 2)
monthly_cat = df.groupby([df['date'].dt.month, 'category'])['total_amount'].sum().unstack(fill_value=0)
monthly_cat.plot(kind='bar', stacked=True, ax=ax2, colormap='Set3')
ax2.set_title('Monthly Sales by Category', fontsize=14, fontweight='bold')
ax2.set_xlabel('Month')
ax2.set_ylabel('Sales ($)')
ax2.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)

# 3. Sales Velocity (Daily trend with moving average)
ax3 = fig2.add_subplot(2, 3, 3)
daily_sales = df.groupby('date')['total_amount'].sum()
rolling_avg = daily_sales.rolling(window=7).mean()
ax3.plot(daily_sales.index, daily_sales.values, alpha=0.3, color='gray', label='Daily Sales')
ax3.plot(rolling_avg.index, rolling_avg.values, color='#E63946', linewidth=2, label='7-Day Moving Average')
ax3.set_title('Sales Trend with Moving Average', fontsize=14, fontweight='bold')
ax3.set_xlabel('Date')
ax3.set_ylabel('Sales ($)')
ax3.legend()
ax3.tick_params(axis='x', rotation=45)

# 4. Category Revenue vs Volume Scatter
ax4 = fig2.add_subplot(2, 3, 4)
cat_summary = df.groupby('category').agg({
    'total_amount': 'sum',
    'quantity': 'sum'
}).reset_index()
ax4.scatter(cat_summary['quantity'], cat_summary['total_amount'],
            s=200, c=range(len(cat_summary)), cmap='viridis', alpha=0.8, edgecolors='black')
for i, txt in enumerate(cat_summary['category']):
    ax4.annotate(txt, (cat_summary['quantity'].iloc[i], cat_summary['total_amount'].iloc[i]),
                 xytext=(5, 5), textcoords='offset points', fontsize=9)
ax4.set_title('Revenue vs Volume by Category', fontsize=14, fontweight='bold')
ax4.set_xlabel('Total Units Sold')
ax4.set_ylabel('Total Revenue ($)')

# 5. Sales by Hour of Day — bimodal probability distribution
#    Weekday: peaks at lunch (12-13) and after-work (17-19)
#    Weekend: single broad midday peak (11-15)
ax5 = fig2.add_subplot(2, 3, 5)
rng = np.random.default_rng(42)  # isolated RNG so global seed(42) state is unaffected

hours = np.arange(8, 21)  # 8 am – 8 pm

# Weekday: bimodal — lunch dip between peaks
weekday_weights = np.array([0.04, 0.06, 0.10, 0.14, 0.08, 0.05, 0.12, 0.18, 0.14, 0.10, 0.07, 0.06, 0.06])
weekday_weights /= weekday_weights.sum()

# Weekend: unimodal, broad midday peak
weekend_weights = np.array([0.03, 0.05, 0.09, 0.13, 0.15, 0.15, 0.13, 0.10, 0.07, 0.05, 0.03, 0.02, 0.01])
weekend_weights /= weekend_weights.sum()

n = len(df)
sampled_hours = np.where(
    df['is_weekend'].values,
    rng.choice(hours, size=n, p=weekend_weights),
    rng.choice(hours, size=n, p=weekday_weights)
)
df['hour'] = sampled_hours

hourly_sales = df.groupby('hour')['total_amount'].sum().reindex(hours, fill_value=0)
bar_colors = ['#E76F51' if h in [12, 13, 17, 18, 19] else '#457B9D' for h in hours]
ax5.bar(hourly_sales.index, hourly_sales.values, color=bar_colors, edgecolor='white')
ax5.set_title('Sales by Hour of Day', fontsize=14, fontweight='bold')
ax5.set_xlabel('Hour of Day')
ax5.set_ylabel('Total Sales ($)')
ax5.set_xticks(hours)
# Annotate peak hours
for h, label in [(12, 'Lunch'), (18, 'After-work')]:
    ax5.annotate(label, xy=(h, hourly_sales[h]),
                 xytext=(0, 8), textcoords='offset points',
                 ha='center', fontsize=8, color='#E76F51', fontweight='bold')

# 6. Top 15 Products: Revenue vs Popularity (Bubble Chart)
ax6 = fig2.add_subplot(2, 3, 6)
product_perf = df.groupby('product').agg({
    'total_amount': 'sum',
    'transaction_id': 'nunique'
}).reset_index()
product_perf.columns = ['product', 'revenue', 'transactions']
product_perf = product_perf.sort_values('revenue', ascending=False).head(15)
bubble_sizes = product_perf['transactions'] * 3
ax6.scatter(product_perf['transactions'], product_perf['revenue'],
            s=bubble_sizes, alpha=0.6, c=range(len(product_perf)), cmap='plasma')
ax6.set_title('Top 15 Products: Revenue vs Popularity', fontsize=14, fontweight='bold')
ax6.set_xlabel('Number of Transactions')
ax6.set_ylabel('Revenue ($)')
for i in range(5):
    ax6.annotate(product_perf.iloc[i]['product'],
                 (product_perf.iloc[i]['transactions'], product_perf.iloc[i]['revenue']),
                 xytext=(5, 5), textcoords='offset points', fontsize=8)

plt.tight_layout()
plt.savefig('output/retail_eda_advanced.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("\n✅ Advanced analysis visualizations saved to output/retail_eda_advanced.png")

# =============================================================
# 7. CUSTOMER ANALYSIS VISUALIZATIONS (6-chart)
# =============================================================

fig3 = plt.figure(figsize=(18, 14))
fig3.suptitle('Customer Behavior & RFM Analysis', fontsize=16, fontweight='bold', y=1.01)

# 1. Customer Segment Distribution
ax1 = fig3.add_subplot(2, 3, 1)
seg_order = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'New Customers',
             'At Risk', 'Needs Attention', 'Cannot Lose Them', 'Lost']
seg_plot = rfm['Segment'].value_counts().reindex(seg_order).dropna()
colors_seg = ['#2A9D8F', '#264653', '#457B9D', '#A8DADC',
              '#E76F51', '#F4A261', '#E63946', '#6A4C93']
ax1.bar(seg_plot.index, seg_plot.values, color=colors_seg[:len(seg_plot)], edgecolor='white')
ax1.set_title('Customer Segment Distribution', fontsize=14, fontweight='bold')
ax1.set_xlabel('Segment')
ax1.set_ylabel('Number of Customers')
ax1.tick_params(axis='x', rotation=45)
for bar in ax1.patches:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
             f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9)

# 2. Purchase Frequency Distribution
ax2 = fig3.add_subplot(2, 3, 2)
ax2.hist(rfm['Frequency'], bins=30, color='#2E86AB', edgecolor='white', alpha=0.85)
ax2.axvline(rfm['Frequency'].mean(), color='#E76F51', linestyle='--', linewidth=2,
            label=f"Mean: {rfm['Frequency'].mean():.1f}")
ax2.axvline(rfm['Frequency'].median(), color='#2A9D8F', linestyle='--', linewidth=2,
            label=f"Median: {rfm['Frequency'].median():.0f}")
ax2.set_title('Purchase Frequency Distribution', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number of Transactions per Customer')
ax2.set_ylabel('Number of Customers')
ax2.legend()

# 3. Revenue by Customer Segment
ax3 = fig3.add_subplot(2, 3, 3)
rev_by_seg = rfm.groupby('Segment')['Monetary'].sum().reindex(seg_order).dropna().sort_values(ascending=True)
ax3.barh(rev_by_seg.index, rev_by_seg.values, color='#A23B72', edgecolor='white')
ax3.set_title('Total Revenue by Customer Segment', fontsize=14, fontweight='bold')
ax3.set_xlabel('Total Revenue ($)')
for bar in ax3.patches:
    width = bar.get_width()
    ax3.text(width + 200, bar.get_y() + bar.get_height()/2,
             f'${width:,.0f}', va='center', fontsize=9)

# 4. Customer Lifetime Value Distribution
ax4 = fig3.add_subplot(2, 3, 4)
ax4.hist(rfm['Monetary'], bins=40, color='#6A4C93', edgecolor='white', alpha=0.85)
ax4.axvline(rfm['Monetary'].mean(), color='#E76F51', linestyle='--', linewidth=2,
            label=f"Mean: ${rfm['Monetary'].mean():.2f}")
ax4.axvline(rfm['Monetary'].median(), color='#2A9D8F', linestyle='--', linewidth=2,
            label=f"Median: ${rfm['Monetary'].median():.2f}")
ax4.set_title('Customer Lifetime Value Distribution', fontsize=14, fontweight='bold')
ax4.set_xlabel('Total Spend per Customer ($)')
ax4.set_ylabel('Number of Customers')
ax4.legend()

# 5. Repeat vs One-Time Buyers
ax5 = fig3.add_subplot(2, 3, 5)
one_time = (rfm['Frequency'] == 1).sum()
repeat = (rfm['Frequency'] > 1).sum()
ax5.pie([one_time, repeat],
        labels=[f'One-Time\n({one_time})', f'Repeat\n({repeat})'],
        autopct='%1.1f%%',
        colors=['#E76F51', '#2A9D8F'],
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax5.set_title('One-Time vs Repeat Buyers', fontsize=14, fontweight='bold')

# 6. Top 10 Customers by Revenue
ax6 = fig3.add_subplot(2, 3, 6)
top_customers = rfm.nlargest(10, 'Monetary')[['customer_id', 'Monetary', 'Frequency', 'Segment']]
bars = ax6.barh(top_customers['customer_id'], top_customers['Monetary'], color='#F4A261', edgecolor='white')
ax6.set_title('Top 10 Customers by Revenue', fontsize=14, fontweight='bold')
ax6.set_xlabel('Total Revenue ($)')
for bar in bars:
    width = bar.get_width()
    ax6.text(width + 50, bar.get_y() + bar.get_height()/2,
             f'${width:,.0f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('output/retail_eda_customers.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("\n✅ Customer analysis visualizations saved to output/retail_eda_customers.png")
