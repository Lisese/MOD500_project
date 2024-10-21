import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

def fetch_weather_data():
    with open('weather.json', 'r') as file:
        weather_data = json.load(file)
    
    df = pd.DataFrame(weather_data['data'])
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_weather_data(df):
    fig, ax1 = plt.subplots(figsize=(15, 8))

    # Plot temperature on the left y-axis
    ax1.plot(df['date'], df['tmax'], label='Max Temperature', color='red')
    ax1.plot(df['date'], df['tmin'], label='Min Temperature', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    # Create a second y-axis for precipitation
    ax2 = ax1.twinx()
    ax2.bar(df['date'], df['prcp'], alpha=0.3, label='Precipitation', color='green')
    ax2.set_ylabel('Precipitation (mm)', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('Monthly Weather Data (2014-2024)')
    fig.autofmt_xdate()  # Rotate and align the tick labels
    plt.tight_layout()
    plt.savefig('weather_plot.png')
    plt.close()

def analyze_weather_data(df):
    print("Weather Data Analysis (2014-2024):")
    print("==================================")
    print(f"Average Temperature: {df['tavg'].mean():.1f}°C")
    print(f"Average Max Temperature: {df['tmax'].mean():.1f}°C")
    print(f"Average Min Temperature: {df['tmin'].mean():.1f}°C")
    print(f"Total Precipitation: {df['prcp'].sum():.1f} mm")
    print(f"Average Monthly Precipitation: {df['prcp'].mean():.1f} mm")
    
    hottest_month = df.loc[df['tmax'].idxmax()]
    coldest_month = df.loc[df['tmin'].idxmin()]
    rainiest_month = df.loc[df['prcp'].idxmax()]
    
    print(f"\nHottest month: {hottest_month['date'].strftime('%B %Y')} with max temperature of {hottest_month['tmax']:.1f}°C")
    print(f"Coldest month: {coldest_month['date'].strftime('%B %Y')} with min temperature of {coldest_month['tmin']:.1f}°C")
    print(f"Rainiest month: {rainiest_month['date'].strftime('%B %Y')} with precipitation of {rainiest_month['prcp']:.1f} mm")

if __name__ == "__main__":
    weather_df = fetch_weather_data()
    
    # Remove rows with null values
    weather_df = weather_df.dropna(subset=['tmax', 'tmin', 'prcp'])
    
    plot_weather_data(weather_df)
    analyze_weather_data(weather_df)

    print("\nWeather plot generated: weather_plot.png")
    print("\nHow to use this data:")
    print("1. Analyze seasonal weather patterns to inform the Operational Model decision")
    print("2. Use temperature and precipitation data for Demand Forecasting")
    print("3. Consider weather conditions when deciding on Campervan Types")
    print("4. Use weather data to estimate potential impact on Customer Satisfaction")
