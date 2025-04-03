from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import iniciar_sesion, procesar_cursos

app = FastAPI()

class Opcion(BaseModel):
    opcion: int

@app.get("/")
def home():
    return {"message": "API para extraer datos de cursos"}

@app.post("/cursos/")
def obtener_datos(opcion: Opcion):
    try:
        resultado = procesar_cursos(opcion.opcion)
        return {"message": "Extracción completada", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los cursos: {str(e)}")
