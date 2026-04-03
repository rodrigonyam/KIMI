# Basic Statistics Summary
print("=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

# Numeric columns
print("\nNUMERIC COLUMNS SUMMARY:")
print(df[['quantity', 'unit_price', 'total_amount']].describe().round(2))

# Categorical columns
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
