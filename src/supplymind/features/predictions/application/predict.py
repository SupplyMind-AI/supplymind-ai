from supplymind.features.model_registry.domain.entities import ModelVersion
class PredictShipment:
 def __init__(self,*,runtime,create_shipment,record_prediction,model_registry):self.runtime=runtime;self.create_shipment=create_shipment;self.record_prediction=record_prediction;self.model_registry=model_registry
 async def execute(self,*,external_id,order_date,features,source='manual'):
  s=await self.create_shipment.execute(external_id=external_id,order_date=order_date,source=source,status='predicted',payload=features);r=self.runtime.predict(features);mv=await self._model();p=await self.record_prediction.execute(shipment_id=s.id,model_version_id=mv.id,delayed=r['delayed'],delay_probability=r['delay_probability'],threshold=r['threshold'],risk_level=r['risk_level']);return {'shipment_id':str(s.id),'external_id':s.external_id,**r,'prediction_id':str(p.id)}
 async def _model(self):
  x=await self.model_registry.get_by_name_version(self.runtime.model_name,self.runtime.model_version)
  if x:return await self.model_registry.promote(x.id) if not x.is_champion else x
  x=await self.model_registry.add(ModelVersion(name=self.runtime.model_name,version=self.runtime.model_version,artifact_uri='models/champion',target_column='is_delayed',threshold=self.runtime.threshold,metrics=self.runtime.metadata.get('test_metrics',{}),feature_columns=self.runtime.metadata.get('feature_columns',[]),is_champion=False));return await self.model_registry.promote(x.id)
