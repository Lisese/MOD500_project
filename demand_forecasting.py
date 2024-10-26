import pandas as pd
import numpy as np
import json
from datetime import datetime
import matplotlib.pyplot as plt

def parse_tourism_date(date_str):
    """Parse date string in format 'YYYYMDD' to year and month"""
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    return year, month

def load_tourism_data():
    """Load and combine tourism data from all regions"""
    regions = ['stavanger', 'haugesund', 'ryfylket']
    all_data = []
    
    for region in regions:
        with open(f'tourism_{region}.json', 'r') as f:
            data = json.load(f)
            
            time_periods = data['dataset']['dimension']['Tid']['category']['label']
            values = data['dataset']['value']
            
            records = []
            for idx, value in enumerate(values):
                if value is not None:
                    time_key = list(time_periods.keys())[idx % len(time_periods)]
                    year, month = parse_tourism_date(time_periods[time_key])
                    
                    records.append({
                        'year': year,
                        'month': month,
                        'value': value,
                        'region': region
                    })
            
            all_data.extend(records)
    
    df = pd.DataFrame(all_data)
    
    # Print data range information
    print("\nData Range Information:")
    print(f"Start Year: {df['year'].min()}")
    print(f"End Year: {df['year'].max()}")
    print(f"Total Years: {df['year'].nunique()}")
    
    # Filter out COVID-19 affected years (2020-2021)
    df_filtered = df[~df['year'].isin([2020, 2021])]
    print("\nExcluding COVID years (2020-2021)")
    
    return df_filtered

def determine_season(month):
    """Determine season based on month"""
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:  # 9, 10, 11
        return 'fall'

def analyze_seasonal_patterns(tourism_df):
    """Analyze seasonal patterns in tourism data"""
    # Calculate monthly averages
    monthly_avg = tourism_df.groupby('month')['value'].agg(['mean', 'std']).reset_index()
    monthly_avg['season'] = monthly_avg['month'].apply(determine_season)
    
    # Calculate seasonal averages
    seasonal_avg = tourism_df.copy()
    seasonal_avg['season'] = seasonal_avg['month'].apply(determine_season)
    seasonal_stats = seasonal_avg.groupby('season')['value'].agg(['mean', 'std', 'count'])
    
    # Calculate year-over-year growth by season
    seasonal_avg['year_season'] = seasonal_avg['year'].astype(str) + '_' + seasonal_avg['season']
    yearly_seasonal = seasonal_avg.groupby(['year', 'season'])['value'].mean().reset_index()
    
    return monthly_avg, seasonal_stats, yearly_seasonal

def plot_monthly_patterns(monthly_avg):
    """Plot monthly patterns"""
    plt.figure(figsize=(15, 6))
    
    # Create bar plot
    bars = plt.bar(range(1, 13), monthly_avg['mean'])
    
    # Add error bars
    plt.errorbar(range(1, 13), monthly_avg['mean'], yerr=monthly_avg['std'],
                fmt='none', color='black', capsize=5)
    
    # Color bars by season
    colors = {'winter': 'blue', 'spring': 'green', 'summer': 'red', 'fall': 'orange'}
    for bar, month in zip(bars, range(1, 13)):
        season = determine_season(month)
        bar.set_color(colors[season])
    
    plt.title('Average Monthly Tourism Demand (Excluding COVID Years)')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Tourists')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # Add legend
    legend_elements = [plt.Rectangle((0,0),1,1, color=color, label=season.capitalize())
                      for season, color in colors.items()]
    plt.legend(handles=legend_elements)
    
    plt.savefig('monthly_patterns.png')
    plt.close()

def plot_yearly_seasonal_trends(yearly_seasonal):
    """Plot yearly trends by season"""
    plt.figure(figsize=(15, 6))
    
    colors = {'winter': 'blue', 'spring': 'green', 'summer': 'red', 'fall': 'orange'}
    
    for season in ['winter', 'spring', 'summer', 'fall']:
        season_data = yearly_seasonal[yearly_seasonal['season'] == season]
        plt.plot(season_data['year'], season_data['value'], 
                marker='o', label=season.capitalize(), color=colors[season])
    
    plt.title('Yearly Tourism Demand by Season (Excluding COVID Years)')
    plt.xlabel('Year')
    plt.ylabel('Average Number of Tourists')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('yearly_seasonal_trends.png')
    plt.close()

def main():
    try:
        # Load tourism data
        print("Loading tourism data...")
        tourism_data = load_tourism_data()
        
        # Analyze seasonal patterns
        print("\nAnalyzing seasonal patterns...")
        monthly_avg, seasonal_stats, yearly_seasonal = analyze_seasonal_patterns(tourism_data)
        
        # Plot results
        plot_monthly_patterns(monthly_avg)
        plot_yearly_seasonal_trends(yearly_seasonal)
        
        # Print seasonal statistics
        print("\nSeasonal Statistics:")
        print("===================")
        for season in ['winter', 'spring', 'summer', 'fall']:
            print(f"\n{season.upper()}")
            print(f"Average Demand: {seasonal_stats.loc[season, 'mean']:,.0f}")
            print(f"Standard Deviation: {seasonal_stats.loc[season, 'std']:,.0f}")
            print(f"Number of Observations: {seasonal_stats.loc[season, 'count']:,.0f}")
            print(f"Coefficient of Variation: {(seasonal_stats.loc[season, 'std'] / seasonal_stats.loc[season, 'mean']) * 100:.1f}%")
        
        print("\nVisualizations saved as:")
        print("- 'monthly_patterns.png': Shows average monthly tourism demand")
        print("- 'yearly_seasonal_trends.png': Shows yearly trends by season")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
