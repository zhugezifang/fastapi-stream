import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from document import get_rect, get_binarized_img
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Modelo de datos con Pydantic
class Position(BaseModel):
    link: str

# Crear una instancia de la aplicación FastAPI
app = FastAPI()
# Origen permitido: '*' permite cualquier origen.
# Si solo quieres permitir un origen específico, reemplaza '*' con el origen específico.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes reemplazar "*" con el origen específico de tu aplicación Angular
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Datos de ejemplo
positions_data = [
    {
        "link": "t9pjzZmHq-4",
    }
    # Puedes agregar más datos de ejemplo aquí si es necesario
]

# Operaciones CRUD

# POST method to get the rect of the cropped document
# It requires an `image` in the body of the request
# FastAPI docs : 1. https://fastapi.tiangolo.com/tutorial/body
#                2. https://fastapi.tiangolo.com/tutorial/request-files
@app.post( "/get_rect" )
async def show_image( image : UploadFile = File() ):
    contents = await image.read()
    # Converting the `contents` bytes to an OpenCV Mat
    # Refer this SO answer -> https://stackoverflow.com/a/61345230/13546426
    img = cv2.imdecode( np.fromstring( contents, np.uint8 ), cv2.IMREAD_COLOR)
    rect = get_rect( img )
    return rect

# POST method to binarize the image to give it a
# 'scanned' effect
@app.post( "/binarize" )
async def binarize( image : UploadFile = File() ):
    contents = await image.read()
    img = cv2.imdecode(np.fromstring(contents, np.uint8), cv2.IMREAD_COLOR)
    img = get_binarized_img( img )
    img_bytes = cv2.imencode('.png', img )[1].tobytes()
    return Response( img_bytes , media_type='image/png' )

# Iniciar el servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
