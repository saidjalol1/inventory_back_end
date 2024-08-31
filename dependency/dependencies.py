from fastapi import Depends
from sqlalchemy.orm import Session
from ver_models import user_models
from database.db_conf import get_db
import auth

super_user = Depends(auth.auth_main.is_super_user)
admin_user : user_models.User = Depends(auth.auth_main.is_admin)
user : user_models.User = Depends(auth.auth_main.is_admin)
database_dep : Session = Depends(get_db)