from datetime import datetime,timezone
from sqlalchemy import case,func,or_,select
from supplymind.features.dashboard.domain.schemas import DashboardSummary
from supplymind.features.events.infrastructure.models import EventModel
from supplymind.features.model_registry.infrastructure.models import ModelVersionModel
from supplymind.features.predictions.infrastructure.models import PredictionModel
from supplymind.features.retraining.infrastructure.models import RetrainingJobModel
from supplymind.features.shipments.infrastructure.models import ShipmentModel
class DashboardQueryService:
 def __init__(self,session):self.session=session
 async def summary(self):
  sc=await self.session.scalar(select(func.count()).select_from(ShipmentModel));pc=await self.session.scalar(select(func.count()).select_from(PredictionModel));stats=(await self.session.execute(select(func.avg(case((PredictionModel.delayed.is_(True),1.0),else_=0.0)),func.avg(PredictionModel.delay_probability)))).one();now=datetime.now(timezone.utc);ec=await self.session.scalar(select(func.count()).select_from(EventModel).where(or_(EventModel.starts_at.is_(None),EventModel.starts_at<=now),or_(EventModel.ends_at.is_(None),EventModel.ends_at>=now)));rc=await self.session.scalar(select(func.count()).select_from(RetrainingJobModel).where(RetrainingJobModel.status.in_(['queued','running'])));ch=(await self.session.execute(select(ModelVersionModel).where(ModelVersionModel.is_champion.is_(True)).order_by(ModelVersionModel.created_at.desc()).limit(1))).scalar_one_or_none();return DashboardSummary(shipment_count=int(sc or 0),prediction_count=int(pc or 0),delayed_prediction_rate=float(stats[0] or 0),average_delay_probability=float(stats[1] or 0),active_event_count=int(ec or 0),queued_retraining_jobs=int(rc or 0),champion_model_name=ch.name if ch else None,champion_model_version=ch.version if ch else None)
