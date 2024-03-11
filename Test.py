import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
data = pd.read_csv('da.csv')

# Filter the dataset
filtered_data = data[(data['year'] == 2090) & 
                     (data['commodity_transaction'] == 'Additives and Oxygenates - Exports') & 
                     (data['category'] == 'additives_and_oxygenates')]

# Convert unit to numeric
def convert_unit_to_numeric(row):
    unit = row['unit']
    quantity = row['quantity']
    if 'thousand' in unit:
        return quantity * 1000
    elif 'million' in unit:
        return quantity * 1000000
    # Add more conversions if needed
    else:
        return quantity

# Apply the conversion function to each row and assign the result to a new column
filtered_data['quantity'] = filtered_data.apply(convert_unit_to_numeric, axis=1)

# Plot the data
plt.figure(figsize=(10, 6))
plt.bar(filtered_data['country_or_area'], filtered_data['quantity'])
plt.xlabel('Country')
plt.ylabel('Quantity')
plt.title('Additives and Oxygenates Exports in 2090')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
