import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# pip install sunpy pandas matplotlib requests

# ==================== 1. SOLAR ACTIVITY ====================
from sunpy.net import Fido, attrs as a

def get_major_solar_flares(start_date, end_date):
    """Fetch major (M/X-class) solar flares."""
    print("Fetching solar flare data...")
    result = Fido.search(
        a.Time(start_date, end_date),
        a.hek.FL,
        a.hek.FRM.Name == "SWPC"
    )
    if result:
        df = result['hek'].to_pandas()
        df = df[['event_starttime', 'event_peaktime', 'fl_classvalue']]
        major = df[df['fl_classvalue'].str.startswith(('M', 'X'), na=False)]
        print(f"Found {len(major)} major flares.")
        return major.sort_values(by='event_peaktime').reset_index(drop=True)
    print("No solar data found.")
    return pd.DataFrame()

# ==================== 2. GEOMAGNETIC DATA ====================
def get_newport_magnetic_data(start_date, end_date):
    """Pull magnetic data from USGS."""
    print("Fetching geomagnetic data...")
    base_url = "https://geomag.usgs.gov/ws/data/"
    params = {
        "id": "NMP",
        "starttime": start_date,
        "endtime": end_date,
        "elements": "D,H",
        "format": "json",
        "sampling_period": "60"
    }
    try:
        response = requests.get(base_url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data.get("values", []))
            if not df.empty:
                df.columns = ["timestamp", "declination", "horizontal_intensity"]
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                print(f"Loaded {len(df)} magnetic records.")
                return df
    except Exception as e:
        print(f"Magnetic data error: {e}")
    return pd.DataFrame()

# ==================== 3. ORCA BIOACOUSTICS ====================
def get_salish_sea_orca_data(start_date, end_date, token=None):
    """Query ONC API (token optional for public data)."""
    print("Fetching orca acoustic data...")
    base_url = "https://data.oceannetworks.ca/api/search"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {
        "locationCode": "SVI",
        "deviceCategoryCode": "HYDROPHONE",
        "dateFrom": f"{start_date}T00:00:00.000Z",
        "dateTo": f"{end_date}T23:59:59.999Z",
        "extension": "json"
    }
    try:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            print(f"Loaded {len(df)} orca-related records.")
            return df
    except Exception as e:
        print(f"ONC data error: {e}")
    return pd.DataFrame()

# ==================== 4. LAG ANALYSIS + PLOTTING ====================
def analyze_and_plot(flare_df, mag_df, audio_df, output_file="correlation_results.png"):
    """Run lag analysis and create plot."""
    if flare_df.empty or mag_df.empty or audio_df.empty:
        print("Not enough data to analyze.")
        return pd.DataFrame()
    
    flare_df['event_peaktime'] = pd.to_datetime(flare_df['event_peaktime'], utc=True)
    mag_df['timestamp'] = pd.to_datetime(mag_df['timestamp'], utc=True)
    
    time_col = 'dateFrom' if 'dateFrom' in audio_df.columns else audio_df.columns[0]
    audio_df[time_col] = pd.to_datetime(audio_df[time_col], utc=True)
    
    correlated = []
    for _, flare in flare_df.iterrows():
        flare_time = flare['event_peaktime']
        window_start = flare_time + timedelta(hours=48)
        window_end = flare_time + timedelta(hours=72)
        
        mag_window = mag_df[(mag_df['timestamp'] >= window_start) & (mag_df['timestamp'] <= window_end)]
        significant = mag_window[mag_window['declination'].abs() >= 6.0]
        
        audio_window = audio_df[(audio_df[time_col] >= window_start) & (audio_df[time_col] <= window_end)]
        
        if not significant.empty and not audio_window.empty:
            correlated.append({
                'flare_time': flare_time.date(),
                'flare_class': flare.get('fl_classvalue'),
                'magnetic_spikes': len(significant),
                'orca_events': len(audio_window)
            })
    
    results = pd.DataFrame(correlated)
    
    # Simple plot
    if not results.empty:
        plt.figure(figsize=(10, 6))
        plt.scatter(results['flare_time'], results['orca_events'], s=results['magnetic_spikes']*10, alpha=0.7)
        plt.title("Solar Flares vs Orca Activity (48-72h lag)")
        plt.xlabel("Flare Date")
        plt.ylabel("Orca Acoustic Events")
        plt.grid(True)
        plt.savefig(output_file)
        print(f"Plot saved as {output_file}")
    
    results.to_csv("correlation_results.csv", index=False)
    print("Results saved to correlation_results.csv")
    return results

# ==================== MAIN RUNNER ====================
if __name__ == "__main__":
    # Example: Analyze a recent solar active period (change dates as needed)
    start = "2024-05-01"
    end   = "2024-06-30"
    
    flares = get_major_solar_flares(start, end)
    mag    = get_newport_magnetic_data(start, end)
    orca   = get_salish_sea_orca_data(start, end)   # token=None for public data
    
    results = analyze_and_plot(flares, mag, orca)
    print("\n=== Correlation Results ===")
    print(results)
