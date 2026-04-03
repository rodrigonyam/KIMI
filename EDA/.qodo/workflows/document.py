# Create detailed analysis visualizations

fig2 = plt.figure(figsize=(18, 14))

# 1. Transaction Value Distribution
ax1 = fig2.add_subplot(2, 3, 1)
transaction_totals = df.groupby('transaction_id')['total_amount'].sum()
ax1.hist(transaction_totals, bins=30, color='#264653', edgecolor='white', alpha=0.8)
ax1.axvline(transaction_totals.mean(), color='#E76F51', linestyle='--', linewidth=2, label=f'Mean: ${transaction_totals.mean():.2f}')
ax1.axvline(transaction_totals.median(), color='#2A9D8F', linestyle='--', linewidth=2, label=f'Median: ${transaction_totals.median():.2f}')
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
scatter = ax4.scatter(cat_summary['quantity'], cat_summary['total_amount'], 
                       s=200, c=range(len(cat_summary)), cmap='viridis', alpha=0.8, edgecolors='black')
for i, txt in enumerate(cat_summary['category']):
    ax4.annotate(txt, (cat_summary['quantity'].iloc[i], cat_summary['total_amount'].iloc[i]),
                xytext=(5, 5), textcoords='offset points', fontsize=9)
ax4.set_title('Revenue vs Volume by Category', fontsize=14, fontweight='bold')
ax4.set_xlabel('Total Units Sold')
ax4.set_ylabel('Total Revenue ($)')

# 5. Hourly Pattern (if we had time, we'll simulate)
ax5 = fig2.add_subplot(2, 3, 5)
# Simulate hourly patterns based on day of week
df['hour'] = np.where(df['is_weekend'], 
                       np.random.choice([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], len(df)),
                       np.random.choice([8, 9, 10, 11, 12, 17, 18, 19, 20], len(df)))
hourly_sales = df.groupby('hour')['total_amount'].sum()
ax5.bar(hourly_sales.index, hourly_sales.values, color='#457B9D', edgecolor='white')
ax5.set_title('Sales by Hour of Day (Simulated)', fontsize=14, fontweight='bold')
ax5.set_xlabel('Hour')
ax5.set_ylabel('Total Sales ($)')
ax5.set_xticks(range(8, 21))

# 6. Product Performance Matrix (Top 15 products)
ax6 = fig2.add_subplot(2, 3, 6)
product_perf = df.groupby('product').agg({
    'total_amount': 'sum',
    'transaction_id': 'nunique'
}).reset_index()
product_perf.columns = ['product', 'revenue', 'transactions']
product_perf = product_perf.sort_values('revenue', ascending=False).head(15)

# Create bubble chart
bubble_sizes = product_perf['transactions'] * 3
scatter = ax6.scatter(product_perf['transactions'], product_perf['revenue'], 
                       s=bubble_sizes, alpha=0.6, c=range(len(product_perf)), cmap='plasma')
ax6.set_title('Top 15 Products: Revenue vs Popularity', fontsize=14, fontweight='bold')
ax6.set_xlabel('Number of Transactions')
ax6.set_ylabel('Revenue ($)')

# Add product labels for top 5
for i in range(5):
    ax6.annotate(product_perf.iloc[i]['product'], 
                (product_perf.iloc[i]['transactions'], product_perf.iloc[i]['revenue']),
                xytext=(5, 5), textcoords='offset points', fontsize=8)

plt.tight_layout()
plt.savefig('/mnt/kimi/output/retail_eda_advanced.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ Advanced analysis visualizations saved!")
