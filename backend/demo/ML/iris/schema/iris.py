
from typing import List
from pydantic import BaseModel


class IrisPayload(BaseModel):
    id: int
    sepal_len: float
    sepal_width: float
    petal_len: float
    petal_width: float
    category: str

    class Config:
        orm_mode = True


class TrainParams(BaseModel):
    cluster_number: int


class TrainResult(BaseModel):
    sepal_len: float
    sepal_width: float
    petal_len: float
    petal_width: float
    cluster: int


class PredictParams(BaseModel):
    sepal_len: float
    sepal_width: float
    petal_len: float
    petal_width: float


class PredictResult(BaseModel):
    cluster: int

