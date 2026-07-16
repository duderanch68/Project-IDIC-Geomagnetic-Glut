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

## 🧪 Pipeline Starter Code (Clean & Fixed)

Save the code below as `Pipeline.py`:

```python
import pandas as pd
import requests
from datetime import datetime
# For solar data: pip install sunpy

# ==================== 1. SOLAR ACTIVITY ====================
from sunpy.net import Fido, attrs as a

def get_major_solar_flares(start_date, end_date):
    """Fetch major (M/X-class) solar flares."""
    result = Fido.search(
        a.Time(start_date, end_date),
        a.hek.FL,
        a.hek.FRM.Name == "SWPC"
    )
    if result:
        df = result['hek'].to_pandas()
        df = df[['event_starttime', 'event_peaktime', 'fl_classvalue']]
        major = df[df['fl_classvalue'].str.startswith(('M', 'X'), na=False)]
        return major.sort_values(by='event_peaktime').reset_index(drop=True)
    return pd.DataFrame()

# ==================== 2. GEOMAGNETIC DATA ====================
def get_newport_magnetic_data(start_date, end_date):
    """Pull magnetic data from USGS (Newport, WA)."""
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
                return df
    except Exception as e:
        print(f"Magnetic data error: {e}")
    return pd.DataFrame()

# ==================== 3. ORCA BIOACOUSTICS ====================
def get_salish_sea_orca_data(start_date, end_date, token=None):
    """Query ONC API for Salish Sea hydrophone data."""
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
            return pd.DataFrame(response.json())
    except Exception as e:
        print(f"ONC data error: {e}")
    return pd.DataFrame()

# ==================== 4. LAG ANALYSIS ====================
def merge_and_analyze_lag(flare_df, mag_df, audio_df):
    """Find 48-72 hour correlations."""
    if flare_df.empty or mag_df.empty or audio_df.empty:
        return pd.DataFrame()
    
    flare_df['event_peaktime'] = pd.to_datetime(flare_df['event_peaktime'], utc=True)
    mag_df['timestamp'] = pd.to_datetime(mag_df['timestamp'], utc=True)
    
    time_col = 'dateFrom' if 'dateFrom' in audio_df.columns else audio_df.columns[0]
    audio_df[time_col] = pd.to_datetime(audio_df[time_col], utc=True)
    
    correlated = []
    for _, flare in flare_df.iterrows():
        flare_time = flare['event_peaktime']
        window_start = flare_time + pd.Timedelta(hours=48)
        window_end   = flare_time + pd.Timedelta(hours=72)
        
        mag_window = mag_df[(mag_df['timestamp'] >= window_start) & (mag_df['timestamp'] <= window_end)]
        significant = mag_window[mag_window['declination'].abs() >= 6.0]
        
        audio_window = audio_df[(audio_df[time_col] >= window_start) & (audio_df[time_col] <= window_end)]
        
        if not significant.empty and not audio_window.empty:
            correlated.append({
                'flare_time': flare_time,
                'flare_class': flare.get('fl_classvalue'),
                'magnetic_spikes': len(significant),
                'orca_events': len(audio_window)
            })
    return pd.DataFrame(correlated)

