import pandas as pd

df = pd.read_csv('data/apple_sales_data.csv')

# Datasets only needs basic data wrangling tasks such as changing some
# datatypes and creating a few new variables

# Transform date variable to datetime and create calender month variable
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['month_calender'] = df['sale_date'].dt.to_period('M').dt.to_timestamp()

# Change year column to categorical variable
df['year'] = df['year'].astype('category')

# Create a new revenue variable without discount for comparison
df['revenue_no_discount_usd'] = df['unit_price_usd'] * df['units_sold']

# Save dataset to new csv file for use in dashboard
df.to_csv('data/apple_sales_data_transformed.csv', index=False)