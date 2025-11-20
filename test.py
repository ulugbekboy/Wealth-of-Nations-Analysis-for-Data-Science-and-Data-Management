import wbgapi as wb

print("Hello")
"""
# List available databases (sources)
print(wb.source.info())

# Information on a specific indicator
print(wb.series.info('NY.GDP.PCAP.CD'))  # GDP per capita

# Economies (countries)
print(wb.economy.info(['USA', 'CHN', 'IND']))  # info for targeted economies

# Regions, income groups
print(wb.region.info())
print(wb.income.info())

"""

import pandas as pd

# Simulate two small datasets like World Bank API might return
gdp_df = pd.DataFrame({
    'economy': ['USA', 'CHN', 'IND'],
    '2000': [36290, 959, 450],
    '2001': [37540, 1026, 480]
}).reset_index(drop=True)

life_df = pd.DataFrame({
    'economy': ['USA', 'CHN', 'IND'],
    '2000': [77.1, 71.5, 63.2],
    '2001': [77.3, 71.8, 63.5]
}).reset_index(drop=True)

# Step 1: Melt both
gdp_melted = gdp_df.melt(id_vars=['economy'], var_name='year', value_name='GDP_per_capita')
life_melted = life_df.melt(id_vars=['economy'], var_name='year', value_name='Life_expectancy')

# Step 2: Convert to numeric
gdp_melted['year'] = pd.to_numeric(gdp_melted['year'])
life_melted['year'] = pd.to_numeric(life_melted['year'])

# Step 3: Merge
merged = pd.merge(gdp_melted, life_melted, on=['economy', 'year'], how='outer')

print(merged)

