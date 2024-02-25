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

@app.get("/link/", response_model=List[Position])
async def get_positions():
    return positions_data

@app.put("/link/{position_id}")
async def update_position(position_id: int, position: Position):
    if position_id < 0 or position_id >= len(positions_data):
        raise HTTPException(status_code=404, detail="Posición no encontrada")
    positions_data[position_id] = position.dict()
    return {"message": f"Posición en el índice {position_id} actualizada correctamente"}

# Iniciar el servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
