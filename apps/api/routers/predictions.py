from fastapi import APIRouter,Depends
from apps.api.dependencies import get_champion_runtime, get_model_registry, get_prediction_repository, get_shipment_repository
from apps.api.schemas import PredictionRequest
from supplymind.features.predictions.application.predict import PredictShipment
from supplymind.features.predictions.application.persistence import RecordPrediction
from supplymind.features.shipments.application.use_cases import CreateShipment
router=APIRouter(prefix='/predictions',tags=['predictions'])
@router.post('')
async def predict(req:PredictionRequest,rt=Depends(get_champion_runtime),sr=Depends(get_shipment_repository),pr=Depends(get_prediction_repository),mr=Depends(get_model_registry)):
 return await PredictShipment(runtime=rt,create_shipment=CreateShipment(sr),record_prediction=RecordPrediction(pr),model_registry=mr).execute(external_id=req.external_id,order_date=req.order_date,features=req.features)
