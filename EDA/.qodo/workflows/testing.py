# Create comprehensive visualizations

# Set up the plotting style
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
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax3.text(width + 50, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
             va='center', fontsize=9)

# 4. Sales by Day of Week
ax4 = fig.add_subplot(4, 3, 4)
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_sales = df.groupby('day_of_week')['total_amount'].sum().reindex(dow_order)
bars = ax4.bar(dow_sales.index, dow_sales.values, color=['#F18F01' if d in ['Saturday', 'Sunday'] else '#048A81' for d in dow_sales.index])
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
plt.suptitle('')  # Remove automatic title
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
bars1 = ax7.bar(x - width/2, quarterly_data['Total Sales'], width, label='Total Sales', color='#F4A261')
ax7_twin = ax7.twinx()
bars2 = ax7_twin.bar(x + width/2, quarterly_data['Transactions'], width, label='Transactions', color='#2A9D8F')
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
for i, category in enumerate(df['category'].unique()):
    data = df[df['category'] == category]['unit_price']
    ax8.hist(data, bins=20, alpha=0.6, label=category)
ax8.set_title('Unit Price Distribution by Category', fontsize=14, fontweight='bold')
ax8.set_xlabel('Unit Price ($)')
ax8.set_ylabel('Frequency')
ax8.legend(fontsize=8, loc='upper right')

# 9. Daily Sales Heatmap
ax9 = fig.add_subplot(4, 3, 9)
df['day'] = df['date'].dt.day
df['month_num'] = df['date'].dt.month
pivot_data = df.groupby(['month_num', 'day'])['total_amount'].sum().unstack(fill_value=0)
sns.heatmap(pivot_data.iloc[:6, :15], cmap='YlOrRd', ax=ax9, cbar_kws={'label': 'Sales ($)'})
ax9.set_title('Daily Sales Heatmap (Jan-Jun)', fontsize=14, fontweight='bold')
ax9.set_xlabel('Day of Month')
ax9.set_ylabel('Month')

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
for i, bar in enumerate(bars):
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
plt.savefig('/mnt/kimi/output/retail_eda_overview.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ Comprehensive EDA visualization saved!")
