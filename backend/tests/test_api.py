import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import app
payload=json.loads((Path(__file__).resolve().parents[1]/'test_payload.json').read_text(encoding='utf-8'))
def test_health():
 r=app.test_client().get('/health'); assert r.status_code==200
 assert len(r.get_json()['features'])==5
def test_predict():
 r=app.test_client().post('/predict',json=payload); assert r.status_code==200,r.get_json()
 assert r.get_json()['prediction'] in [1,10,20]
def test_missing():
 p=payload.copy();p.pop('slope_deg');assert app.test_client().post('/predict',json=p).status_code==400
def test_invalid():
 p=payload.copy();p['aspect_deg']=999;assert app.test_client().post('/predict',json=p).status_code==400
