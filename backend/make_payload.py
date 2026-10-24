from pathlib import Path
import json
import pandas as pd
root=Path(__file__).resolve().parents[1]
df=pd.read_csv(root/'data/forest_test_spatial.csv',nrows=1)
row=df.iloc[0]
from math import atan2,degrees
aspect_deg=(degrees(atan2(float(row['aspect_sin']),float(row['aspect_cos'])))+360)%360
payload={k:float(row[k]) for k in ['elevation_m','slope_deg','temp_mean_c','precip_total_mm']}
payload['aspect_deg']=aspect_deg
(root/'backend/test_payload.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print('Saved backend/test_payload.json (no target variable)')
