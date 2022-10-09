from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship

from demo.db.base_class import Base


class Iris(Base):
    id = Column(Integer, primary_key=True, index=True)
    sepal_len = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_len = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    category = Column(String, nullable=False)


