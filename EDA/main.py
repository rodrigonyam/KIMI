# Retail Store EDA - Consolidated Analysis Script
# Covers: data generation, descriptive stats, business insights,
#         comprehensive visualizations, and advanced analysis.

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Precompute series used across multiple charts
category_sales = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).reset_index()
category_sales.columns = ['category', 'total_amount']

monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum().reset_index()
monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()

product_revenue = df.groupby('product')['total_amount'].sum().sort_values(ascending=False).head(10).reset_index()
product_revenue.columns = ['product', 'revenue']

dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_sales = df.groupby('day_of_week')['total_amount'].sum().reindex(dow_order).reset_index()
dow_sales.columns = ['day_of_week', 'total_amount']
dow_sales['is_weekend'] = dow_sales['day_of_week'].isin(['Saturday', 'Sunday'])

quantity_dist = df['quantity'].value_counts().sort_index().reset_index()
quantity_dist.columns = ['quantity', 'count']

quarterly_data = df.groupby('quarter').agg(
    Total_Sales=('total_amount', 'sum'),
    Transactions=('transaction_id', 'nunique')
).reset_index()

monthly_category_pct = (
    df.groupby([df['date'].dt.to_period('M'), 'category'])['total_amount']
    .sum().unstack(fill_value=0)
)
monthly_category_pct = monthly_category_pct.div(monthly_category_pct.sum(axis=1), axis=0) * 100
monthly_category_pct.index = monthly_category_pct.index.to_timestamp()
monthly_category_pct = monthly_category_pct.reset_index().melt(id_vars='date', var_name='category', value_name='pct')

avg_transaction = df.groupby('category')['total_amount'].mean().sort_values().reset_index()
avg_transaction.columns = ['category', 'avg_amount']

df['week'] = df['date'].dt.isocalendar().week.astype(int)
df['dow_num'] = df['date'].dt.dayofweek
pivot_weekly = df.groupby(['dow_num', 'week'])['total_amount'].sum().unstack(fill_value=0)
dow_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
pivot_weekly.index = dow_labels[:len(pivot_weekly)]

corr_data = df[['quantity', 'unit_price', 'total_amount']].corr().round(2)

fig_overview = make_subplots(
    rows=4, cols=3,
    subplot_titles=[
        'Total Sales by Category',
        'Monthly Sales Trend (2025)',
        'Top 10 Products by Revenue',
        'Sales by Day of Week',
        'Transaction Amount by Category (Box)',
        'Quantity per Transaction',
        'Quarterly Sales vs Transactions',
        'Unit Price Distribution by Category',
        'Weekly Sales Rhythm (Full Year)',
        'Category Market Share Over Time (%)',
        'Avg Transaction Value by Category',
        'Correlation Matrix',
    ],
    specs=[
        [{'type': 'domain'}, {'type': 'xy'}, {'type': 'xy'}],
        [{'type': 'xy'},     {'type': 'xy'}, {'type': 'xy'}],
        [{'type': 'xy'},     {'type': 'xy'}, {'type': 'xy'}],
        [{'type': 'xy'},     {'type': 'xy'}, {'type': 'xy'}],
    ],
    vertical_spacing=0.08,
    horizontal_spacing=0.08,
)

# 1. Pie – sales by category
fig_overview.add_trace(
    go.Pie(labels=category_sales['category'], values=category_sales['total_amount'],
           textinfo='percent+label', hole=0.3, showlegend=False),
    row=1, col=1
)

# 2. Monthly trend line+fill
fig_overview.add_trace(
    go.Scatter(x=monthly_sales['date'], y=monthly_sales['total_amount'],
               mode='lines+markers', fill='tozeroy',
               line=dict(color='#2E86AB', width=2), name='Monthly Sales'),
    row=1, col=2
)

# 3. Top-10 products horizontal bar
fig_overview.add_trace(
    go.Bar(x=product_revenue['revenue'], y=product_revenue['product'],
           orientation='h', marker_color='#A23B72',
           text=product_revenue['revenue'].map('${:,.0f}'.format),
           textposition='outside', showlegend=False),
    row=1, col=3
)

# 4. Day-of-week bar
fig_overview.add_trace(
    go.Bar(x=dow_sales['day_of_week'], y=dow_sales['total_amount'],
           marker_color=dow_sales['is_weekend'].map({True: '#F18F01', False: '#048A81'}),
           text=dow_sales['total_amount'].map('${:,.0f}'.format),
           textposition='outside', showlegend=False),
    row=2, col=1
)

# 5. Box plot per category
for cat in df['category'].unique():
    fig_overview.add_trace(
        go.Box(y=df.loc[df['category'] == cat, 'total_amount'],
               name=cat, showlegend=False, boxpoints=False),
        row=2, col=2
    )

# 6. Quantity distribution bar
fig_overview.add_trace(
    go.Bar(x=quantity_dist['quantity'], y=quantity_dist['count'],
           marker_color='#6A4C93',
           text=quantity_dist['count'], textposition='outside', showlegend=False),
    row=2, col=3
)

# 7. Quarterly dual bar (Sales left axis, Transactions right axis via secondary_y workaround)
fig_overview.add_trace(
    go.Bar(x=quarterly_data['quarter'], y=quarterly_data['Total_Sales'],
           name='Total Sales', marker_color='#F4A261',
           text=quarterly_data['Total_Sales'].map('${:,.0f}'.format),
           textposition='outside'),
    row=3, col=1
)
fig_overview.add_trace(
    go.Bar(x=quarterly_data['quarter'], y=quarterly_data['Transactions'],
           name='Transactions', marker_color='#2A9D8F',
           text=quarterly_data['Transactions'], textposition='outside'),
    row=3, col=1
)

# 8. Price histogram per category (overlaid)
for cat in df['category'].unique():
    fig_overview.add_trace(
        go.Histogram(x=df.loc[df['category'] == cat, 'unit_price'],
                     name=cat, opacity=0.6, nbinsx=20, showlegend=False),
        row=3, col=2
    )

# 9. Weekly heatmap
fig_overview.add_trace(
    go.Heatmap(
        z=pivot_weekly.values,
        x=pivot_weekly.columns.tolist(),
        y=pivot_weekly.index.tolist(),
        colorscale='YlOrRd',
        colorbar=dict(title='Sales ($)', len=0.25, y=0.38),
        showscale=True,
    ),
    row=3, col=3
)

# 10. Category market share area chart
for cat in monthly_category_pct['category'].unique():
    sub = monthly_category_pct[monthly_category_pct['category'] == cat]
    fig_overview.add_trace(
        go.Scatter(x=sub['date'], y=sub['pct'],
                   name=cat, stackgroup='one', mode='none',
                   fill='tonexty', showlegend=False),
        row=4, col=1
    )

# 11. Avg transaction value horizontal bar
fig_overview.add_trace(
    go.Bar(x=avg_transaction['avg_amount'], y=avg_transaction['category'],
           orientation='h', marker_color='#E76F51',
           text=avg_transaction['avg_amount'].map('${:.2f}'.format),
           textposition='outside', showlegend=False),
    row=4, col=2
)

# 12. Correlation heatmap
fig_overview.add_trace(
    go.Heatmap(
        z=corr_data.values,
        x=corr_data.columns.tolist(),
        y=corr_data.index.tolist(),
        colorscale='RdBu',
        zmid=0,
        text=corr_data.values,
        texttemplate='%{text:.2f}',
        showscale=False,
    ),
    row=4, col=3
)

fig_overview.update_layout(
    height=1800,
    title_text='Retail Store EDA — Overview (2025)',
    title_font_size=20,
    template='plotly_white',
    barmode='group',
)
fig_overview.write_html('output/retail_eda_overview.html')
fig_overview.show()
print("\n✅ Interactive overview saved to output/retail_eda_overview.html")

# =============================================================
# 6. ADVANCED ANALYSIS VISUALIZATIONS (6-chart)
# =============================================================

# Precompute
transaction_totals = df.groupby('transaction_id')['total_amount'].sum().reset_index()
transaction_totals.columns = ['transaction_id', 'value']
txn_mean = transaction_totals['value'].mean()
txn_median = transaction_totals['value'].median()

month_labels = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
monthly_cat = (
    df.groupby([df['date'].dt.month, 'category'])['total_amount']
    .sum().reset_index()
)
monthly_cat.columns = ['month_num', 'category', 'sales']
monthly_cat['month'] = monthly_cat['month_num'].map(month_labels)

daily_sales = df.groupby('date')['total_amount'].sum().reset_index()
daily_sales.columns = ['date', 'sales']
daily_sales['rolling_7'] = daily_sales['sales'].rolling(window=7).mean()

cat_summary = df.groupby('category').agg(
    total_revenue=('total_amount', 'sum'),
    total_units=('quantity', 'sum')
).reset_index()

# Hourly simulation
rng = np.random.default_rng(42)
hours = np.arange(8, 21)
weekday_weights = np.array([0.04, 0.06, 0.10, 0.14, 0.08, 0.05, 0.12, 0.18, 0.14, 0.10, 0.07, 0.06, 0.06])
weekday_weights /= weekday_weights.sum()
weekend_weights = np.array([0.03, 0.05, 0.09, 0.13, 0.15, 0.15, 0.13, 0.10, 0.07, 0.05, 0.03, 0.02, 0.01])
weekend_weights /= weekend_weights.sum()
n = len(df)
sampled_hours = np.where(
    df['is_weekend'].values,
    rng.choice(hours, size=n, p=weekend_weights),
    rng.choice(hours, size=n, p=weekday_weights)
)
df['hour'] = sampled_hours
hourly_sales = df.groupby('hour')['total_amount'].sum().reindex(hours, fill_value=0).reset_index()
hourly_sales.columns = ['hour', 'sales']
hourly_sales['peak'] = hourly_sales['hour'].isin([12, 13, 17, 18, 19])

product_perf = df.groupby('product').agg(
    revenue=('total_amount', 'sum'),
    transactions=('transaction_id', 'nunique')
).reset_index().sort_values('revenue', ascending=False).head(15)

fig_adv = make_subplots(
    rows=2, cols=3,
    subplot_titles=[
        'Transaction Value Distribution',
        'Monthly Sales by Category',
        'Sales Trend — 7-Day Moving Average',
        'Revenue vs Volume by Category',
        'Sales by Hour of Day',
        'Top 15 Products: Revenue vs Popularity',
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.1,
)

# 1. Transaction value histogram + mean/median lines
fig_adv.add_trace(
    go.Histogram(x=transaction_totals['value'], nbinsx=30,
                 marker_color='#264653', opacity=0.85, name='Transactions', showlegend=False),
    row=1, col=1
)
for val, label, color in [(txn_mean, f'Mean ${txn_mean:.2f}', '#E76F51'),
                           (txn_median, f'Median ${txn_median:.2f}', '#2A9D8F')]:
    fig_adv.add_vline(x=val, line_dash='dash', line_color=color,
                      annotation_text=label, annotation_position='top right',
                      row=1, col=1)

# 2. Monthly stacked bar by category
for cat in monthly_cat['category'].unique():
    sub = monthly_cat[monthly_cat['category'] == cat].sort_values('month_num')
    fig_adv.add_trace(
        go.Bar(x=sub['month'], y=sub['sales'], name=cat, showlegend=True),
        row=1, col=2
    )
fig_adv.update_layout(barmode='stack')

# 3. Daily + 7-day rolling average
fig_adv.add_trace(
    go.Scatter(x=daily_sales['date'], y=daily_sales['sales'],
               mode='lines', line=dict(color='lightgray', width=1),
               name='Daily Sales', showlegend=False, opacity=0.5),
    row=1, col=3
)
fig_adv.add_trace(
    go.Scatter(x=daily_sales['date'], y=daily_sales['rolling_7'],
               mode='lines', line=dict(color='#E63946', width=2),
               name='7-Day MA', showlegend=False),
    row=1, col=3
)

# 4. Scatter: revenue vs units per category
fig_adv.add_trace(
    go.Scatter(
        x=cat_summary['total_units'], y=cat_summary['total_revenue'],
        mode='markers+text',
        text=cat_summary['category'],
        textposition='top center',
        marker=dict(size=18, color=list(range(len(cat_summary))),
                    colorscale='Viridis', showscale=False, opacity=0.85,
                    line=dict(width=1, color='black')),
        showlegend=False,
    ),
    row=2, col=1
)

# 5. Hourly bar chart
fig_adv.add_trace(
    go.Bar(
        x=hourly_sales['hour'], y=hourly_sales['sales'],
        marker_color=hourly_sales['peak'].map({True: '#E76F51', False: '#457B9D'}),
        text=hourly_sales['sales'].map('${:,.0f}'.format),
        textposition='outside',
        showlegend=False,
        customdata=hourly_sales['peak'],
    ),
    row=2, col=2
)
for h, label in [(12, 'Lunch'), (18, 'After-work')]:
    h_val = hourly_sales.loc[hourly_sales['hour'] == h, 'sales'].values[0]
    fig_adv.add_annotation(
        x=h, y=h_val, text=label, showarrow=True, arrowhead=2,
        ax=0, ay=-30, font=dict(color='#E76F51', size=10),
        row=2, col=2
    )

# 6. Bubble chart: top 15 products
fig_adv.add_trace(
    go.Scatter(
        x=product_perf['transactions'], y=product_perf['revenue'],
        mode='markers+text',
        text=product_perf['product'],
        textposition='top center',
        marker=dict(
            size=product_perf['transactions'] / product_perf['transactions'].max() * 50 + 8,
            color=list(range(len(product_perf))),
            colorscale='Plasma', showscale=False, opacity=0.7,
        ),
        showlegend=False,
    ),
    row=2, col=3
)

fig_adv.update_xaxes(title_text='Transaction Value ($)', row=1, col=1)
fig_adv.update_yaxes(title_text='Frequency', row=1, col=1)
fig_adv.update_xaxes(title_text='Month', row=1, col=2)
fig_adv.update_yaxes(title_text='Sales ($)', row=1, col=2)
fig_adv.update_xaxes(title_text='Date', row=1, col=3)
fig_adv.update_yaxes(title_text='Sales ($)', row=1, col=3)
fig_adv.update_xaxes(title_text='Total Units Sold', row=2, col=1)
fig_adv.update_yaxes(title_text='Total Revenue ($)', row=2, col=1)
fig_adv.update_xaxes(title_text='Hour of Day', row=2, col=2)
fig_adv.update_yaxes(title_text='Total Sales ($)', row=2, col=2)
fig_adv.update_xaxes(title_text='Number of Transactions', row=2, col=3)
fig_adv.update_yaxes(title_text='Revenue ($)', row=2, col=3)

fig_adv.update_layout(
    height=900,
    title_text='Retail Store EDA — Advanced Analysis (2025)',
    title_font_size=20,
    template='plotly_white',
    legend_title_text='Category',
)
fig_adv.write_html('output/retail_eda_advanced.html')
fig_adv.show()
print("\n✅ Interactive advanced analysis saved to output/retail_eda_advanced.html")

# =============================================================
# 7. CUSTOMER ANALYSIS VISUALIZATIONS (6-chart)
# =============================================================

seg_order = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'New Customers',
             'At Risk', 'Needs Attention', 'Cannot Lose Them', 'Lost']
seg_colors = ['#2A9D8F', '#264653', '#457B9D', '#A8DADC',
              '#E76F51', '#F4A261', '#E63946', '#6A4C93']
color_map = dict(zip(seg_order, seg_colors))

seg_plot = rfm['Segment'].value_counts().reindex(seg_order).dropna().reset_index()
seg_plot.columns = ['Segment', 'count']

rev_by_seg = (
    rfm.groupby('Segment')['Monetary'].sum()
    .reindex(seg_order).dropna().sort_values(ascending=True)
    .reset_index()
)
rev_by_seg.columns = ['Segment', 'Revenue']

one_time = int((rfm['Frequency'] == 1).sum())
repeat = int((rfm['Frequency'] > 1).sum())

top_customers = rfm.nlargest(10, 'Monetary')[['customer_id', 'Monetary', 'Frequency', 'Segment']].copy()
top_customers = top_customers.sort_values('Monetary', ascending=True)

fig_cust = make_subplots(
    rows=2, cols=3,
    subplot_titles=[
        'Customer Segment Distribution',
        'Purchase Frequency Distribution',
        'Total Revenue by Customer Segment',
        'Customer Lifetime Value Distribution',
        'One-Time vs Repeat Buyers',
        'Top 10 Customers by Revenue',
    ],
    specs=[
        [{'type': 'xy'},     {'type': 'xy'},     {'type': 'xy'}],
        [{'type': 'xy'},     {'type': 'domain'}, {'type': 'xy'}],
    ],
    vertical_spacing=0.14,
    horizontal_spacing=0.1,
)

# 1. Segment bar chart
fig_cust.add_trace(
    go.Bar(
        x=seg_plot['Segment'], y=seg_plot['count'],
        marker_color=[color_map.get(s, '#888') for s in seg_plot['Segment']],
        text=seg_plot['count'], textposition='outside',
        showlegend=False,
    ),
    row=1, col=1
)

# 2. Purchase frequency histogram + mean/median
freq_mean = rfm['Frequency'].mean()
freq_median = rfm['Frequency'].median()
fig_cust.add_trace(
    go.Histogram(x=rfm['Frequency'], nbinsx=30,
                 marker_color='#2E86AB', opacity=0.85, showlegend=False),
    row=1, col=2
)
for val, label, color in [(freq_mean, f'Mean {freq_mean:.1f}', '#E76F51'),
                           (freq_median, f'Median {freq_median:.0f}', '#2A9D8F')]:
    fig_cust.add_vline(x=val, line_dash='dash', line_color=color,
                       annotation_text=label, annotation_position='top right',
                       row=1, col=2)

# 3. Revenue by segment horizontal bar
fig_cust.add_trace(
    go.Bar(
        x=rev_by_seg['Revenue'], y=rev_by_seg['Segment'],
        orientation='h',
        marker_color=[color_map.get(s, '#888') for s in rev_by_seg['Segment']],
        text=rev_by_seg['Revenue'].map('${:,.0f}'.format),
        textposition='outside',
        showlegend=False,
    ),
    row=1, col=3
)

# 4. CLV (Monetary) histogram + mean/median
mon_mean = rfm['Monetary'].mean()
mon_median = rfm['Monetary'].median()
fig_cust.add_trace(
    go.Histogram(x=rfm['Monetary'], nbinsx=40,
                 marker_color='#6A4C93', opacity=0.85, showlegend=False),
    row=2, col=1
)
for val, label, color in [(mon_mean, f'Mean ${mon_mean:.0f}', '#E76F51'),
                           (mon_median, f'Median ${mon_median:.0f}', '#2A9D8F')]:
    fig_cust.add_vline(x=val, line_dash='dash', line_color=color,
                       annotation_text=label, annotation_position='top right',
                       row=2, col=1)

# 5. One-time vs repeat pie
fig_cust.add_trace(
    go.Pie(
        labels=[f'One-Time ({one_time})', f'Repeat ({repeat})'],
        values=[one_time, repeat],
        marker_colors=['#E76F51', '#2A9D8F'],
        textinfo='percent+label',
        hole=0.35,
        showlegend=False,
    ),
    row=2, col=2
)

# 6. Top-10 customers horizontal bar
fig_cust.add_trace(
    go.Bar(
        x=top_customers['Monetary'], y=top_customers['customer_id'],
        orientation='h',
        marker_color='#F4A261',
        text=top_customers['Monetary'].map('${:,.0f}'.format),
        textposition='outside',
        customdata=top_customers[['Frequency', 'Segment']].values,
        hovertemplate='<b>%{y}</b><br>Revenue: %{x:$,.0f}<br>Visits: %{customdata[0]}<br>Segment: %{customdata[1]}<extra></extra>',
        showlegend=False,
    ),
    row=2, col=3
)

fig_cust.update_xaxes(title_text='Number of Customers', row=1, col=1)
fig_cust.update_xaxes(title_text='Transactions per Customer', row=1, col=2)
fig_cust.update_yaxes(title_text='Number of Customers', row=1, col=2)
fig_cust.update_xaxes(title_text='Total Revenue ($)', row=1, col=3)
fig_cust.update_xaxes(title_text='Total Spend ($)', row=2, col=1)
fig_cust.update_yaxes(title_text='Number of Customers', row=2, col=1)
fig_cust.update_xaxes(title_text='Total Revenue ($)', row=2, col=3)

fig_cust.update_layout(
    height=900,
    title_text='Retail Store EDA — Customer Behavior & RFM (2025)',
    title_font_size=20,
    template='plotly_white',
)
fig_cust.write_html('output/retail_eda_customers.html')
fig_cust.show()
print("\n✅ Interactive customer analysis saved to output/retail_eda_customers.html")
