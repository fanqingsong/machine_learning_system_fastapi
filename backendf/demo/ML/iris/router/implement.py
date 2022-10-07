from fastapi import APIRouter, Depends
from starlette.requests import Request
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from demo.db.session import ActiveSession
from demo.core import security

from demo.ML.iris.schema.iris import (IrisPayload)
from demo.ML.iris.models.iris import Iris

# from demo.package1.house_price.schema.prediction import HousePredictionResult
#
# from demo.package1.house_price.service import HousePriceModel
#
# from fastapi_hive.ioc_framework.module_container import ModuleContainer

router = APIRouter()


@router.get("/iris", response_model=List[IrisPayload], name="iris")
def get_all_iris(
        request: Request,
        authenticated: bool = Depends(security.validate_request),
        session: Session = ActiveSession
) -> List[IrisPayload]:
    contents = session.execute(select(Iris)).all()
    return contents

#
# @router.post("/predict", response_model=HousePredictionResult, name="predict")
# def post_predict(
#     request: Request,
#     authenticated: bool = Depends(security.validate_request),
#     block_data: HousePredictionPayload = None
# ) -> HousePredictionResult:
#
#     module_container: ModuleContainer = request.app.state.module_container
#     model: HousePriceModel = module_container.get_module("house_price").service
#     prediction: HousePredictionResult = model.predict(block_data)
#
#     return prediction
