from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import time

# Suppress future warnings regarding downcasting
pd.set_option('future.no_silent_downcasting', True)

# Initialize pytrends with increased timeout
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))

# Expanded keyword groups including rental/hire and non-rental related searches
norway_group1 = [
    'camper van rental norway', 
    'motorhome rental norway', 
    'camper rental norway',
    'van rental norway', 
    'rv hire norway'
]

norway_group2 = [
    'camper hire norway', 
    'rent a camper van norway', 
    'rent motorhome norway', 
    'hire rv norway', 
    'camper van holiday norway'
]

norway_group3 = [
    'camper van norway', 
    'motorhome norway', 
    'rv norway', 
    'van life norway', 
    'camper trip norway'
]

norway_group4 = [
    'camping norway', 
    'caravan norway', 
    'norwegian camping sites', 
    'road trip norway', 
    'touring norway with a camper'
]

norway_group5 = [
    'camper van adventure norway', 
    'outdoor norway camper', 
    'norway travel van', 
    'explore norway camper', 
    'camper tour norway'
]

stavanger_group1 = [
    'camper van rental stavanger', 
    'motorhome rental stavanger', 
    'camper rental stavanger',
    'rv rental stavanger', 
    'van hire stavanger'
]

stavanger_group2 = [
    'camper hire stavanger', 
    'rent a motorhome stavanger', 
    'camper van hire stavanger', 
    'rent a camper stavanger', 
    'motorhome holiday stavanger'
]

stavanger_group3 = [
    'camper van stavanger', 
    'motorhome stavanger', 
    'rv stavanger', 
    'camper trip stavanger', 
    'camper van trip stavanger'
]

stavanger_group4 = [
    'camping stavanger', 
    'caravan stavanger', 
    'outdoor stavanger camper', 
    'explore stavanger van', 
    'stavanger camper sites'
]

stavanger_group5 = [
    'camper van tour stavanger', 
    'travel stavanger camper', 
    'camper van adventure stavanger', 
    'exploring stavanger by camper', 
    'camper holiday stavanger'
]

# No specific geo parameter to get global trends tied to the keywords
timeframe = '2016-01-01 2024-10-01'  # From January 2016 to October 2024
category = 0  # Use category 0 for all categories
gprop = ''  # Use '' for web search

# Function to fetch data for a group of keywords with retry and delay
def fetch_group_trends_data(group_name, keywords, max_retries=3, delay=10):
    attempts = 0
    while attempts < max_retries:
        try:
            # Build the payload for the current group of keywords
            pytrends.build_payload(keywords, timeframe=timeframe, cat=category, gprop=gprop)
            print(f"Fetching data for {group_name} with keywords: {keywords}")

            # Fetch interest over time
            interest_over_time = pytrends.interest_over_time()
            if not interest_over_time.empty:
                # Sum up the total interest for all keywords in this group
                total_interest = interest_over_time.drop(columns=['isPartial']).sum(axis=1)
                return total_interest
            else:
                print(f"No data found for {group_name} with keywords: {keywords}")
                return None
        except Exception as e:
            print(f"Error fetching data for {group_name} with keywords {keywords}: {e}")
            if '429' in str(e):
                attempts += 1
                print(f"Retrying in {delay} seconds... (Attempt {attempts}/{max_retries})")
                time.sleep(delay)  # Wait before retrying
            else:
                return None
    print(f"Failed to fetch data for {group_name} after {max_retries} attempts.")
    return None

# Store interest data from all groups
aggregated_data = {
    'Date': [],
    'Norway_Total_Interest': [],
    'Stavanger_Total_Interest': []
}

# Fetch and aggregate data for Norway groups
norway_total_interest = []

# Iterate over all Norway groups
norway_groups = [
    (norway_group1, "Norway Group 1"),
    (norway_group2, "Norway Group 2"),
    (norway_group3, "Norway Group 3"),
    (norway_group4, "Norway Group 4"),
    (norway_group5, "Norway Group 5")
]

for group in norway_groups:
    data = fetch_group_trends_data(group[1], group[0])
    if data is not None:
        norway_total_interest.append(data)

# Combine Norway data if successful
if norway_total_interest:
    combined_norway_interest = pd.concat(norway_total_interest, axis=1).sum(axis=1)  # Sum the interest across all groups

# Fetch and aggregate data for Stavanger groups
stavanger_total_interest = []

# Iterate over all Stavanger groups
stavanger_groups = [
    (stavanger_group1, "Stavanger Group 1"),
    (stavanger_group2, "Stavanger Group 2"),
    (stavanger_group3, "Stavanger Group 3"),
    (stavanger_group4, "Stavanger Group 4"),
    (stavanger_group5, "Stavanger Group 5")
]

for group in stavanger_groups:
    data = fetch_group_trends_data(group[1], group[0])
    if data is not None:
        stavanger_total_interest.append(data)

# Combine Stavanger data if successful
if stavanger_total_interest:
    combined_stavanger_interest = pd.concat(stavanger_total_interest, axis=1).sum(axis=1)  # Sum the interest across all groups

# Resample data to monthly and store in a CSV file
if norway_total_interest and stavanger_total_interest:
    # Resample to monthly-end data
    combined_norway_interest = combined_norway_interest.resample('ME').mean()
    combined_stavanger_interest = combined_stavanger_interest.resample('ME').mean()
    
    # Prepare data for CSV
    aggregated_data['Date'] = combined_norway_interest.index
    aggregated_data['Norway_Total_Interest'] = combined_norway_interest.values
    aggregated_data['Stavanger_Total_Interest'] = combined_stavanger_interest.values

    # Create a DataFrame and save to CSV
    result_df = pd.DataFrame(aggregated_data)
    output_file = 'aggregated_camper_van_interest.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

    # Plot the data
    plt.figure(figsize=(12, 8))
    plt.plot(result_df['Date'], result_df['Norway_Total_Interest'], label='Norway Total Interest', marker='o')
    plt.plot(result_df['Date'], result_df['Stavanger_Total_Interest'], label='Stavanger Total Interest', marker='x')
    
    # Formatting the plot
    plt.title('Camper Van Rental Interest Over Time')
    plt.xlabel('Date')
    plt.ylabel('Interest Count')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()
else:
    print("No aggregated data found for Norway or Stavanger.")
