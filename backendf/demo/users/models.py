
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from demo.db.base_class import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass



