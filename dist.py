import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('MCPD_Bias_Incidents.csv')

# Remove 'ID' and '# of Victims' columns
df = df.drop(columns=['ID', '# of Victims'])

# Convert 'Incident Date' to datetime format
df['Incident Date'] = pd.to_datetime(df['Incident Date'], format='%m/%d/%Y')

# Show unique 'Victim Type' and allow user to select one category by number
unique_victim_types = df['Victim Type'].unique()
print("Select a Victim Type:")
for i, victim_type in enumerate(unique_victim_types):
    print(f"{i}: {victim_type}")

selected_index = int(input("Enter the number corresponding to the Victim Type: "))
selected_victim_type = unique_victim_types[selected_index]

# Filter data by selected victim type
df = df[df['Victim Type'] == selected_victim_type]

# Sum instances per unique 'Bias Code' by month
df['Month-Year'] = df['Incident Date'].dt.to_period('M')
monthly_bias_code_counts = df.groupby(['Month-Year', 'Bias Code']).size().unstack(fill_value=0)

# Sort data based on 'Incident Date'
monthly_bias_code_counts = monthly_bias_code_counts.sort_index()

# Select top 4 'Bias Code' based on the number of incidents
top_4_bias_codes = monthly_bias_code_counts.sum().nlargest(4).index
monthly_bias_code_counts_top_4 = monthly_bias_code_counts[top_4_bias_codes]

# Plot the data
plt.figure(figsize=(14, 8))
linestyles = ['-', '--', '-.', ':']

for i, bias_code in enumerate(top_4_bias_codes):
    linestyle = linestyles[i % len(linestyles)]
    plt.plot(monthly_bias_code_counts_top_4.index.to_timestamp(), monthly_bias_code_counts_top_4[bias_code], 
             label=bias_code, linestyle=linestyle, color='black')

plt.title(f'Bias Incidents for {selected_victim_type}')
plt.xlabel('Month-Year')
plt.ylabel('Number of Incidents')
plt.xticks(rotation=90)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b-%Y'))
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the figure
filename = f"Bias_Incidents_for_{selected_victim_type.replace('/', '_')}.png"
plt.savefig(filename)

plt.show()

