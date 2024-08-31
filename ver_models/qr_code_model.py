from pydantic import BaseModel


class QrCode(BaseModel):
    number : str
    

class QrCodeOut(QrCode):
    id : int
    qr_code_image : str