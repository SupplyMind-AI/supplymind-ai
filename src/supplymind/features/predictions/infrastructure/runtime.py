from __future__ import annotations
import json
from pathlib import Path
import joblib,pandas as pd
class ChampionModelRuntime:
 def __init__(self,model_directory:str|Path)->None:
  d=Path(model_directory);mp=d/'model.joblib';meta=d/'metadata.json'
  if not mp.exists() or not meta.exists():raise FileNotFoundError(f'Champion artifact incomplete: {d}')
  self.pipeline=joblib.load(mp);self.metadata=json.loads(meta.read_text())
 @property
 def threshold(self):return float(self.metadata.get('threshold',.5))
 @property
 def model_name(self):return str(self.metadata.get('model_name','champion'))
 @property
 def model_version(self):return str(self.metadata.get('model_version','1.0.0'))
 def predict(self,features:dict)->dict:
  p=float(self.pipeline.predict_proba(pd.DataFrame([features]))[0,1]);return {'delayed':p>=self.threshold,'delay_probability':p,'threshold':self.threshold,'risk_level':'high' if p>=.7 else 'medium' if p>=.4 else 'low','model_name':self.model_name,'model_version':self.model_version}
