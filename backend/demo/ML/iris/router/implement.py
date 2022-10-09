import logging

from fastapi import APIRouter, Depends
from starlette.requests import Request
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from demo.db.session import get_session
from demo.core import security
from loguru import logger

from demo.ML.iris.schema.iris import (IrisPayload)
from demo.ML.iris.models.iris import Iris
from demo.ML.iris.schema import iris as schema

from sklearn.cluster import KMeans
from sklearn.externals import joblib


router = APIRouter()


@router.get("/all_data", response_model=List[IrisPayload], name="all iris data")
def get_all_iris(
        request: Request,
        session: Session = Depends(get_session)
) -> List[IrisPayload]:
    # logger.info("=================")
    # return "sss"
    contents = session.execute(select(Iris)).scalars().all()
    # logger.info("------------------------!!!!!!!!!!!!!!!!!!!!!!")
    # logger.info(contents)
    # logger.info(contents[0].__dict__)

    return contents


@router.post("/trainer", response_model=List[schema.TrainResult], name="trainer")
def get_all_iris(
        train_params: schema.TrainParams,
        session: Session = Depends(get_session)
) -> List[schema.TrainResult]:
    cluster_number = train_params.cluster_number

    logger.info(f"cluster number = {cluster_number}")

    model = KMeans(n_clusters=cluster_number)

    iris_orm = session.execute(select(Iris)).scalars().all()
    iris_pydantic = [IrisPayload.from_orm(one) for one in iris_orm]
    iris_array = [[one.sepal_len, one.sepal_width, one.petal_len, one.petal_width] for one in iris_pydantic]

    model.fit(iris_array)

    # save model for prediction
    joblib.dump(model, 'model.kmeans')

    # test saved prediction
    model = joblib.load('model.kmeans')

    # cluster result
    labels = model.predict(iris_array)

    print("cluster result")
    print(labels)

    # transfer data to client
    iris_dict = [
        {"sepal_len": oneIris.sepal_len, "sepal_width": oneIris.sepal_width, "petal_len": oneIris.petal_len,
         "petal_width": oneIris.petal_width}
        for oneIris in iris_pydantic
    ]

    for i in range(0, len(iris_dict)):
        iris_dict[i]["cluster"] = labels[i]

    return iris_dict


@router.post("/predictor", response_model=schema.PredictResult, name="predictor")
def get_all_iris(
        predict_params: schema.PredictParams,
        session: Session = Depends(get_session)
):
    petal_len = predict_params.petal_len
    petal_width = predict_params.petal_width
    sepal_len = predict_params.sepal_len
    sepal_width = predict_params.sepal_width

    iris_arrary = [[sepal_len, sepal_width, petal_len, petal_width]]

    # test saved prediction
    model = joblib.load('model.kmeans')

    # cluster result
    labels = model.predict(iris_arrary)

    print("cluster result")
    print(labels)

    # transfer data to client
    result = {
        "cluster": labels[0]
    }

    return result


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
