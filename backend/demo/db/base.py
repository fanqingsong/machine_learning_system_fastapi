# Import all the models, so that Base has them before being
# imported by Alembic
from demo.db.base_class import Base  # noqa
from demo.ML.iris.models.iris import Iris  # noqa
from demo.users.models import User

