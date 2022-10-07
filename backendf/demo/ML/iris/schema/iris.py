
from typing import List
from pydantic import BaseModel


class IrisPayload(BaseModel):
    id: int
    sepal_len: float
    sepal_width: float
    petal_len: float
    petal_width: float
    category: str


def payload_to_list(hpp: IrisPayload) -> List:
    return [
        hpp.id,
        hpp.sepal_len,
        hpp.sepal_width,
        hpp.petal_len,
        hpp.petal_width,
        hpp.category,
    ]
