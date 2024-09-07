import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency

# Load the dataset
df = pd.read_csv('MCPD_Bias_Incidents.csv')

# Remove 'ID' and '# of Victims' columns
df.drop(['ID', '# of Victims'], axis=1, inplace=True)

# Convert 'Incident Date' to datetime format
df['Incident Date'] = pd.to_datetime(df['Incident Date'], format='%m/%d/%Y')

print(df['Bias Code'].unique())
print(len(df['Bias Code'].unique()))
print(df['Bias'].unique())
print(len(df['Bias'].unique()))

# Show unique 'Victim Type' and allow user to select one category
unique_victim_types = df['Victim Type'].unique()
print("Select a Victim Type by number:")
for i, vt in enumerate(unique_victim_types):
    print(f"{i}: {vt}")

selected_index = int(input("Enter the number of the selected Victim Type: "))
selected_victim_type = unique_victim_types[selected_index]

# Filter data by selected 'Victim Type'
df_filtered = df[df['Victim Type'] == selected_victim_type]

# Sum instances per unique 'Bias Code' by month
df_filtered['Month-Year'] = df_filtered['Incident Date'].dt.to_period('M')
monthly_bias_code_counts = df_filtered.groupby(['Month-Year', 'Bias Code']).size().unstack(fill_value=0)

# Sort data based on 'Incident Date'
monthly_bias_code_counts.sort_index(inplace=True)

# Calculate chi-squared values and p-values for each month-year period
determinants_1 = ['Incident Date', 'District', 'Bias Code', 'Bias']
determinants_2 = ['Status', '# of Suspects', 'Suspect Known/Unknown']
chi_squared_values_1 = []
p_values_1 = []
chi_squared_values_2 = []
p_values_2 = []

for period in monthly_bias_code_counts.index:
    period_data = df_filtered[df_filtered['Month-Year'] == period]
    chi2_values_1 = []
    p_vals_1 = []
    chi2_values_2 = []
    p_vals_2 = []
    for determinant in determinants_1:
        if period_data[determinant].nunique() > 1:  # Check if there is more than one unique value
            contingency_table = pd.crosstab(period_data['Bias Code'], period_data[determinant])
            if contingency_table.size > 0:  # Check if the contingency table is not empty
                chi2, p, _, _ = chi2_contingency(contingency_table)
                chi2_values_1.append(chi2 if p < 0.05 else np.nan)
                p_vals_1.append(p)
            else:
                chi2_values_1.append(np.nan)
                p_vals_1.append(np.nan)
        else:
            chi2_values_1.append(np.nan)
            p_vals_1.append(np.nan)
    for determinant in determinants_2:
        if period_data[determinant].nunique() > 1:  # Check if there is more than one unique value
            contingency_table = pd.crosstab(period_data['Bias Code'], period_data[determinant])
            if contingency_table.size > 0:  # Check if the contingency table is not empty
                chi2, p, _, _ = chi2_contingency(contingency_table)
                chi2_values_2.append(chi2 if p < 0.05 else np.nan)
                p_vals_2.append(p)
            else:
                chi2_values_2.append(np.nan)
                p_vals_2.append(np.nan)
        else:
            chi2_values_2.append(np.nan)
            p_vals_2.append(np.nan)
    chi_squared_values_1.append(chi2_values_1)
    p_values_1.append(p_vals_1)
    chi_squared_values_2.append(chi2_values_2)
    p_values_2.append(p_vals_2)

# Convert lists to arrays for plotting
chi_squared_values_1 = np.array(chi_squared_values_1)
p_values_1 = np.array(p_values_1)
chi_squared_values_2 = np.array(chi_squared_values_2)
p_values_2 = np.array(p_values_2)

# Define combined linestyles and widths
styles = [(ls, lw) for ls in ['-', '--', '-.', ':'] for lw in [1, 2]]

# Plotting the first graph
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Chi-squared values for the first graph
for i, determinant in enumerate(determinants_1):
    ax1.plot(monthly_bias_code_counts.index.astype(str), chi_squared_values_1[:, i], 
             label=f'Chi-squared ({determinant})', 
             linestyle=styles[i][0], 
             linewidth=styles[i][1], 
             color='black')

ax1.set_xlabel('Month-Year')
ax1.set_ylabel('Chi-squared Values')
ax1.tick_params(axis='x', rotation=90)
ax1.set_xticks(np.arange(0, len(monthly_bias_code_counts.index), step=15))

# Add legend inside the graph
ax1.legend(loc='upper left')

# Save the first graph
safe_victim_type = selected_victim_type.replace("/", "_")
fig1.savefig(f'graph1_{safe_victim_type}.png', dpi=300)

#fig1.savefig(f'graph1_{selected_victim_type}.png', dpi=300)

# Plotting the second graph
fig2, ax2 = plt.subplots(figsize=(12, 6))

# Chi-squared values for the second graph
for i, determinant in enumerate(determinants_2):
    ax2.plot(monthly_bias_code_counts.index.astype(str), chi_squared_values_2[:, i], 
             label=f'Chi-squared ({determinant})', 
             linestyle=styles[i][0], 
             linewidth=styles[i][1], 
             color='black')

ax2.set_xlabel('Month-Year')
ax2.set_ylabel('Chi-squared Values')
ax2.tick_params(axis='x', rotation=90)
ax2.set_xticks(np.arange(0, len(monthly_bias_code_counts.index), step=15))

# Add legend inside the graph
ax2.legend(loc='upper left')

# Save the second graph
#fig2.savefig(f'graph2_{selected_victim_type}.png', dpi=300)
fig2.savefig(f'graph2_{safe_victim_type}.png', dpi=300)

