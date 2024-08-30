import models
import pydantics
from database.db_conf import get_db

class CreateObject:
    def __init__(self, model,database, object):
        self.model = model,
        self.database = database
        self.object = object
        
    def create(self):
        _object = self.model(**object.model_dumb())
        self.database.add(_object)
        self.database.commit()
        self.database.refresh(_object)
        print(_object)
        return _object