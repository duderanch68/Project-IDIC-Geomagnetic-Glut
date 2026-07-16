markdown 

# Project: The IDIC Marine Ecology Framework 

### The Geomagnetic Glut Hypothesis: Connecting Solar Maxima, Lunar Dynamics, and Orca Cultural Fads 

 

* **Author:** Jeffrey A. LeClair Jr. 

* **Permanent CERN DOI:** [10.5281/zenodo.21347876](https://zenodo.org) 

* **Status:** Open-Source Software Request / Immediate Co-Authorship Offered 

 

--- 

 

## 📢 Call for Data Engineers & Co-Authors 

 

The conceptual physics and environmental architecture of this framework are completely locked and permanently timestamped under a registered CERN DOI [5.1].  

 

**The Objective:** We are building an open-source Python pipeline to automate data aggregation and generate our validation charts. The developer or team that successfully writes the script to pull these data points and plot the historical correlation will receive **Permanent Co-Author Credit** on the master publication file. 

 

--- 

 

## 🛠️ Developer Technical Specifications 

 

We require an automated Python script (`pandas`, `matplotlib`/`seaborn`) that queries, clean-merges, and plots data across three open-source APIs to isolate our predicted 48-to-72-hour lag window. 

 

### Required API Implementations: 

1. **Solar Activity Input:** Query `SunPy` to fetch historical GOES Satellite X-ray flux and Coronal Mass Ejection (CME) alerts. 

2. **Geomagnetic Grid Fluctuations:** Utilize the USGS `Geomag-Algorithms` or `MagPy` library to pull regional magnetic declination logs (specifically tracking 6-degree local shifts near the Newport, Washington observatory array). 

3. **Bioacoustic/Sighting Timestamps:** Use the `onc` Python client library to query the Ocean Networks Canada Oceans 3.0 API, extracting continuous acoustic event metadata and orca social communication density timestamps in the Salish Sea. 

 

--- 

 

## 🔬 The Core Hypothesis 

 

### 1. The Sun-Earth-Moon Circuit 

The Sun acts as a planetary power generator, Earth functions as a giant electromagnet, and the Moon serves as a structural regulator by mechanically stirring the liquid iron core and pulling on upper atmospheric plasma tides. Under Solar Maximum conditions, major CMEs overload the circuit, shattering the steady magnetic background rhythm. 

 

### 2. The Magnetic Salmon Bottleneck 

Migrating salmon utilize microscopic clusters of magnetite in their nasal cavities to interpret Earth's grid lines for natal homing. A 6-degree regional geomagnetic tilt short-circuits this internal compass. Unable to locate river-mouth coordinates, the migrating biomass is forced into localized, dense bottlenecks in coastal estuaries and bays. 

 

### 3. Existential Luxury & Non-Human Ritual 

When localized prey density spikes, hunting effort drops to zero. This grants apex predators (*Orcinus orca*) immediate **cognitive slack** and profound boredom. This psychological environmental shift channels their high intelligence into creative play, status manipulation, and arbitrary social copying—triggering viral cultural fads (e.g., the historic "salmon hat" phenomena) and maritime defensive reactions (e.g., Iberian rudder strikes targeting localized metallic EMF signatures). 

 

--- 

 

## 🚀 How to Contribute and Join the Project 

1. **Fork** this repository.

markdown## 🧪 Open-Source Starter Code Architecture

To fast-track development, the baseline API connection scripts have been structured below. Developers can use these snippets as the foundation for the automated pipeline.

### Pipeline 1: Solar Activity Input (SunPy)
```python
import pandas as pd
from sunpy.net import Fido, attrs as a

def get_goes_solar_flares(start_date, end_date):
    """Queries SunPy for GOES Satellite X-ray flux events."""
    result = Fido.search(
        a.Time(start_date, end_date),
        a.hek.FL,
        a.hek.FRM.Name == "SWPC"
    )
    if result:
        df = result['hek'].to_pandas()
        clean_df = df[['event_starttime', 'event_peaktime', 'fl_classvalue']]
        major_flares = clean_df[clean_df['fl_classvalue'].str.startswith(('M', 'X'), na=False)]
        return major_flares.sort_values(by='event_starttime')
    return None
```

#pythonimport pandas as pd
import requests


def get_newport_magnetic_data(start_date, end_date):
    """Tracks local magnetic variations near Newport, WA (NMP) via USGS API."""
    url = "https://usgs.gov"
    params = {
        "id": "NMP",  # Newport Observatory Code
        "starttime": start_date,
        "endtime": end_date,
        "elements": "D,H",  # D = Declination, H = Horizontal Intensity
        "format": "json",
        "sampling_period": "60",  # 1-minute intervals to catch spikes
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["values"])
        df.columns = ["timestamp", "declination", "horizontal_intensity"]
        return df
    return None


def get_salish_sea_orca_audio(start_date, end_date, api_token="YOUR_TOKEN"):
    """Extracts bioacoustic event metadata and orca communication timestamps from ONC."""
    url = "https://oceannetworks.ca"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = {
        "locationCode": "SVI",  # Strait of Georgia / Salish Sea Array
        "deviceCategoryCode": "HYDROPHONE",
        "dateFrom": start_date,  # Format: YYYY-MM-DDTHH:mm:ss.fffZ
        "dateTo": end_date,
        "extension": "json",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    return None
  
```

### 🎯 Next Milestones for Contributors:
1. **Time-Series Alignment:** Clean and synchronize the timestamps across all three datasets.
2. **Lag Identification:** Isolate the exact 48-to-72-hour delay window between an X-Class flare peak and an uptick in regional orca social vocalization density.
3. **Visualization:** Plot the final correlation graphs (`matplotlib` / `seaborn`) to append to the main Zenodo publication.

3. Build the data pipeline script using the target client libraries. 

4. Open a **Pull Request** displaying your generated correlation graphs.  

5. Once verified, you will be formally added to the Zenodo DOI publication file as a Core Technical Architect. '''python
text### Pipeline 4: Time-Series Merging Logic

```python
def merge_and_analyze_lag(flare_df, mag_df, audio_df):
    """Aligns timestamps across all three datasets and isolates the 48-to-72 hour lag window."""
    # Step 1: Standardize all dataframe timestamps to UTC datetime objects
    flare_df['event_peaktime'] = pd.to_datetime(flare_df['event_peaktime'], utc=True)
    mag_df['timestamp'] = pd.to_datetime(mag_df['timestamp'], utc=True)
    audio_df['dateFrom'] = pd.to_datetime(audio_df['dateFrom'], utc=True)
    
    correlated_events = []
    
    # Step 2: Loop through each major solar flare event
    for idx, flare in flare_df.iterrows():
        flare_time = flare['event_peaktime']
        
        # Define our targeted 48-to-72-hour reaction window
        window_start = flare_time + pd.Timedelta(hours=48)
        window_end = flare_time + pd.Timedelta(hours=72)
        
        # Step 3: Check for regional 6-degree magnetic spikes inside that window
        mag_window = mag_df[(mag_df['timestamp'] >= window_start) & (mag_df['timestamp'] <= window_end)]
        significant_tilts = mag_window[mag_window['declination'].abs() >= 6.0]
        
        # Step 4: Check for Orca vocalization surges inside the exact same window
        audio_window = audio_df[(audio_df['dateFrom'] >= window_start) & (audio_df['dateFrom'] <= window_end)]
        
        # If both physical triggers align, capture the matching dataset for plotting
        if not significant_tilts.empty and not audio_window.empty:
            correlated_events.append({
                'flare_time': flare_time,
                'flare_class': flare['fl_classvalue'],
                'magnetic_spikes': len(significant_tilts),
                'orca_vocal_density': len(audio_window)
            })
            
    return pd.DataFrame(correlated_events)
```
