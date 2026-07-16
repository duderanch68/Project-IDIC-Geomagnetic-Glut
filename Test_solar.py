import pandas as pd
from sunpy.net import Fido, attrs as a
from datetime import datetime

# Fetch recent major solar flares
result = Fido.search(
    a.Time("2024-01-01", "2025-07-01"),  # adjust dates
    a.hek.FL,
    a.hek.FRM.Name == "SWPC"
)

if result:
    df = result['hek'].to_pandas()
    major = df[df['fl_classvalue'].str.startswith(('M', 'X'), na=False)]
    print(major[['event_peaktime', 'fl_classvalue']])
else:
    print("No data or error")
