import os
import models
from my_util_functions.qr_code import generate_qr_code
from ver_models import qr_code_model
from typing import List
from fastapi import APIRouter
from dependency.dependencies import super_user, admin_user, user, database_dep


code_path = APIRouter(
    prefix="/qrcode",
    tags=["Qr code routes"]
)


@code_path.post("/generate", response_model=qr_code_model.QrCodeOut)
async def generate(code: qr_code_model.QrCode, db = database_dep, us = admin_user):
    try:
        _qr_code = models.QrCode(number=code.number)
        db.add(_qr_code)
        db.commit()
        db.refresh(_qr_code)

        qr_code_filename = f"{code.number}.png"
        qr_code_path = os.path.join("static/qrcodes/", qr_code_filename)
        generate_qr_code(_qr_code.id, qr_code_path)
        _qr_code.qr_code_image = qr_code_path

        db.commit()
        db.refresh(_qr_code)
        return _qr_code
    except Exception as e:
        return {"error": str(e)}


@code_path.get("/get/all", response_model=List[qr_code_model.QrCodeOut])
async def get_all(db = database_dep):
    _qr_codes = db.query(models.QrCode).all()
    return _qr_codes


@code_path.delete("/delete/{id}")
async def get_all(id:int,db = database_dep):
    _qr_codes = db.query(models.QrCode).filter(models.QrCode.id == id).first()
    db.delete(_qr_codes)
    db.commit()
    return {"message":"O'chirildi"}