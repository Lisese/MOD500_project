import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

def fetch_tourism_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    region = list(data['dataset']['dimension']['Region']['category']['label'].values())[0]
    accommodations = list(data['dataset']['dimension']['InnKvartering1']['category']['label'].values())
    years = list(data['dataset']['dimension']['Tid']['category']['label'].values())
    nationalities = list(data['dataset']['dimension']['Landkoder2']['category']['label'].values())
    values = data['dataset']['value']
    
    df = pd.DataFrame({
        'value': values,
        'Region': [region] * len(values),
        'Accommodation': accommodations * (len(values) // len(accommodations)),
        'Year': years * len(accommodations) * len(nationalities),
        'Nationality': nationalities * len(years) * len(accommodations)
    })
    
    df['Year'] = pd.to_datetime(df['Year'], format='%YM%m')
    return df

def plot_total_tourists(dfs):
    plt.figure(figsize=(12, 6))
    for df in dfs:
        region = df['Region'].iloc[0]
        df_total = df.groupby('Year')['value'].sum()
        plt.plot(df_total.index, df_total.values, marker='o', label=region)
    
    plt.title('Total Tourists by Region')
    plt.xlabel('Year')
    plt.ylabel('Number of Overnight Stays')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('total_tourists_by_region.png')
    plt.close()

def plot_accommodation_comparison(df):
    region = df['Region'].iloc[0]
    df_pivot = df.pivot_table(index='Year', columns='Accommodation', values='value', aggfunc='sum')
    
    plt.figure(figsize=(12, 6))
    for column in df_pivot.columns:
        plt.plot(df_pivot.index, df_pivot[column], marker='o', label=column)
    
    plt.title(f'Accommodation Comparison - {region}')
    plt.xlabel('Year')
    plt.ylabel('Number of Overnight Stays')
    plt.legend(title='Accommodation Type')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    safe_filename = ''.join(e for e in region if e.isalnum() or e in [' ', '_']).rstrip().replace(' ', '_')
    plt.savefig(f'accommodation_comparison_{safe_filename}.png')
    plt.close()

def plot_nationality_comparison(df):
    region = df['Region'].iloc[0]
    df_pivot = df.pivot_table(index='Year', columns='Nationality', values='value', aggfunc='sum')
    
    plt.figure(figsize=(12, 6))
    for column in df_pivot.columns:
        plt.plot(df_pivot.index, df_pivot[column], marker='o', label=column)
    
    plt.title(f'Nationality Comparison - {region}')
    plt.xlabel('Year')
    plt.ylabel('Number of Overnight Stays')
    plt.legend(title='Nationality')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    safe_filename = ''.join(e for e in region if e.isalnum() or e in [' ', '_']).rstrip().replace(' ', '_')
    plt.savefig(f'nationality_comparison_{safe_filename}.png')
    plt.close()

def analyze_seasonality(df):
    df['Month'] = df['Year'].dt.month
    monthly_avg = df.groupby(['Month', 'Nationality'])['value'].mean().unstack()
    
    plt.figure(figsize=(12, 6))
    for column in monthly_avg.columns:
        plt.plot(monthly_avg.index, monthly_avg[column], marker='o', label=column)
    
    plt.title(f'Average Monthly Tourists by Nationality - {df["Region"].iloc[0]}')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Overnight Stays')
    plt.legend(title='Nationality')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(True)
    plt.tight_layout()
    safe_filename = ''.join(e for e in df["Region"].iloc[0] if e.isalnum() or e in [' ', '_']).rstrip().replace(' ', '_')
    plt.savefig(f'seasonality_{safe_filename}.png')
    plt.close()

if __name__ == "__main__":
    json_files = ['tourism_stavanger.json', 'tourism_haugesund.json', 'tourism_ryfylket.json']
    dataframes = []

    for file in json_files:
        print(f"Processing file: {file}")
        df = fetch_tourism_data(file)
        if df is not None and not df.empty:
            dataframes.append(df)

    if dataframes:
        plot_total_tourists(dataframes)
        for df in dataframes:
            plot_accommodation_comparison(df)
            plot_nationality_comparison(df)
            analyze_seasonality(df)

        combined_df = pd.concat(dataframes)
        
        print("Tourism Data Analysis Summary:")
        print("==============================")
        print("1. Total Overnight Stays by Region (Last Year):")
        print(combined_df[combined_df['Year'].dt.year == combined_df['Year'].dt.year.max()].groupby('Region')['value'].sum())
        
        print("\n2. Year-over-Year Growth by Region (Last Year):")
        yoy_growth = combined_df.groupby(['Region', combined_df['Year'].dt.year])['value'].sum().unstack()
        yoy_growth = (yoy_growth[yoy_growth.columns[-1]] / yoy_growth[yoy_growth.columns[-2]] - 1)
        print(yoy_growth)
        
        print("\n3. Most Popular Accommodation Type by Region:")
        print(combined_df.groupby(['Region', 'Accommodation'])['value'].sum().groupby(level=0).idxmax())
        
        print("\nPlots generated:")
        print("1. total_tourists_by_region.png")
        for df in dataframes:
            safe_filename = ''.join(e for e in df['Region'].iloc[0] if e.isalnum() or e in [' ', '_']).rstrip().replace(' ', '_')
            print(f"2. accommodation_comparison_{safe_filename}.png")
            print(f"3. nationality_comparison_{safe_filename}.png")
            print(f"4. seasonality_{safe_filename}.png")

        print("\nHow to use this data:")
        print("1. Analyze trends in tourism across different regions to inform the Business Launch Decision")
        print("2. Compare the popularity of hotels vs. camping sites to guide your service offerings")
        print("3. Use the total tourist numbers and growth rates to estimate potential market size for your Pricing Strategy")
        print("4. Consider seasonal variations in the data to decide on your Operational Model")
        print("5. Use the regional comparisons to determine the most promising locations for your business")
        print("6. Analyze the nationality comparison to target specific markets and tailor your marketing strategies")
    else:
        print("Failed to fetch tourism data. Please check your JSON files and try again.")
