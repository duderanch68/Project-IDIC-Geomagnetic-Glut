markdown

# Project: The IDIC Marine Ecology Framework

### The Geomagnetic Glut Hypothesis: Connecting Solar Maxima, Lunar Dynamics, and Orca Cultural Fads

**Author:** Jeffrey A. LeClair Jr.  
**Permanent CERN DOI:** [10.5281/zenodo.21347876](https://zenodo.org)  
**Status:** Open-Source Software Request / Immediate Co-Authorship Offered

---

## 📢 Call for Data Engineers & Co-Authors

The conceptual physics and environmental architecture of this framework are permanently timestamped under the registered CERN DOI.

**The Objective:** Build an open-source Python pipeline that automatically pulls, cleans, merges, and plots the three key datasets to test the predicted **48-to-72-hour lag** between solar events and orca behavioral changes. The developer(s) who deliver working, validated correlation charts will receive **permanent co-author credit** on the master publication.

---

## 🛠️ Developer Technical Specifications

We need a Python script using `pandas`, `matplotlib`/`seaborn` that:
1. Queries historical solar flare/CME data
2. Pulls regional geomagnetic variation data
3. Pulls Salish Sea orca acoustic/sighting data
4. Aligns everything and isolates the 48–72 hour lag window

### Required Data Sources:

1. **Solar Activity** — SunPy library (GOES X-ray flux & major flares)
2. **Geomagnetic Fluctuations** — USGS geomagnetic observatories (focus on Newport, WA area)
3. **Orca Bioacoustics** — Ocean Networks Canada (ONC) Oceans 3.0 API

---

## 🔬 The Core Hypothesis

### 1. The Sun-Earth-Moon Circuit
The Sun powers the system, Earth acts as a giant electromagnet, and the Moon regulates it. During Solar Maximum, major CMEs overload and disrupt the steady magnetic rhythm.

### 2. The Magnetic Salmon Bottleneck
Salmon use magnetite crystals and cryptochrome proteins for navigation. A significant regional geomagnetic shift (~6°) disrupts their internal compass, causing prey to bottleneck in coastal areas.

### 3. Existential Luxury & Non-Human Ritual
Easy prey → reduced hunting effort for orcas → cognitive slack → increased play, social copying, and cultural fads (e.g., "salmon hat" phenomenon).

---

## 🧪 Pipeline Starter Code (Updated & Fixed)

Copy these functions into `Pipeline.py` as a starting point.

```python
import pandas as pd
from datetime import datetime
import requests
# sunpy is recommended for solar data (pip install sunpy)

# ==================== 1. SOLAR ACTIVITY ====================
from sunpy.net import Fido, attrs as a

def get_major_solar_flares(start_date, end_date):
    """Fetch major (M/X-class) solar flares using SunPy."""
    result = Fido.search(
        a.Time(start_date, end_date),
        a.hek.FL,
        a.hek.FRM.Name == "SWPC"
    )
    if result:
        df = result['hek'].to_pandas()
        df = df[['event_starttime', 'event_peaktime', 'fl_classvalue']]
        major_flares = df[df['fl_classvalue'].str.startswith(('M', 'X'), na=False)]
        return major_flares.sort_values(by='event_peaktime').reset_index(drop=True)
    return pd.DataFrame()

# ==================== 2. GEOMAGNETIC DATA ====================
def get_newport_magnetic_data(start_date, end_date):
    """Pull magnetic declination data from USGS (Newport Observatory)."""
    # Real USGS Geomagnetism API endpoint example
    base_url = "https://geomag.usgs.gov/ws/data/"
    params = {
        "id": "NMP",                    # Newport, WA
        "starttime": start_date,
        "endtime": end_date,
        "elements": "D,H",              # D = Declination, H = Horizontal intensity
        "format": "json",
        "sampling_period": "60"         # minutes
    }
    try:
        response = requests.get(base_url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data.get("values", []))
            if not df.empty:
                df.columns = ["timestamp", "declination", "horizontal_intensity"]
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
    except Exception as e:
        print(f"Error fetching magnetic data: {e}")
    return pd.DataFrame()

# ==================== 3. ORCA BIOACOUSTICS ====================
def get_salish_sea_orca_data(start_date, end_date, token=None):
    """Query ONC Oceans 3.0 API for hydrophone data in Salish Sea."""
    base_url = "https://data.oceannetworks.ca/api/search"
    # You will need a free ONC token for full access
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {
        "locationCode": "SVI",           # Strait of Georgia / Salish Sea
        "deviceCategoryCode": "HYDROPHONE",
        "dateFrom": f"{start_date}T00:00:00.000Z",
        "dateTo": f"{end_date}T23:59:59.999Z",
        "extension": "json"
    }
    try:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching ONC data: {e}")
    return pd.DataFrame()

# ==================== 4. LAG ANALYSIS ====================
def merge_and_analyze_lag(flare_df, mag_df, audio_df):
    """Align datasets and find 48-72 hour correlations."""
    if flare_df.empty or mag_df.empty or audio_df.empty:
        return pd.DataFrame()
    
    # Standardize timestamps
    flare_df['event_peaktime'] = pd.to_datetime(flare_df['event_peaktime'], utc=True)
    mag_df['timestamp'] = pd.to_datetime(mag_df['timestamp'], utc=True)
    # Adjust column name based on actual ONC output
    time_col = 'dateFrom' if 'dateFrom' in audio_df.columns else audio_df.columns[0]
    audio_df[time_col] = pd.to_datetime(audio_df[time_col], utc=True)
    
    correlated_events = []
    
    for _, flare in flare_df.iterrows():
        flare_time = flare['event_peaktime']
        window_start = flare_time + pd.Timedelta(hours=48)
        window_end = flare_time + pd.Timedelta(hours=72)
        
        # Check for significant magnetic shifts
        mag_window = mag_df[(mag_df['timestamp'] >= window_start) & 
                           (mag_df['timestamp'] <= window_end)]
        significant_tilts = mag_window[mag_window['declination'].abs() >= 6.0]
        
        # Check for orca vocalization/activity increase
        audio_window = audio_df[(audio_df[time_col] >= window_start) & 
                               (audio_df[time_col] <= window_end)]
        
        if not significant_tilts.empty and not audio_window.empty:
            correlated_events.append({
                'flare_time': flare_time,
                'flare_class': flare['fl_classvalue'],
                'magnetic_spikes': len(significant_tilts),
                'orca_events': len(audio_window),
                'lag_hours': (window_start - flare_time).total_seconds() / 3600
            })
    
    return pd.DataFrame(correlated_events)

