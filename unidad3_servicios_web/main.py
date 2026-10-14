from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI(title="API de estudiantes", version="1.0.0")
class Estudiante(BaseModel):
    numero_control: str = Field(min_length=5, max_length=20)
    nombre: str = Field(min_length=3, max_length=100)
    carrera: str = Field(min_length=3, max_length=120)
    


estudiantes_db = {
 "91650064": {
 "numero_control": "91650064",
 "nombre": "Juan Pérez",
 "carrera": "Sistemas Computacionales"
 },
 "91650065": {
 "numero_control": "91650065",
 "nombre": "María López",
 "carrera": "Sistemas Computacionales"
 }
}

@app.get("/")
def inicio():
 return {"mensaje": "API escolar disponible"}

@app.get("/api/v1/estudiantes")
def listar_estudiantes():
 return list(estudiantes_db.values())

@app.get("/api/v1/estudiantes/{numero_control}")
def obtener_estudiante(numero_control: str):
 estudiante = estudiantes_db.get(numero_control)
 if estudiante is None:
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")
 return estudiante

@app.post("/api/v1/estudiantes", status_code=201)
def crear_estudiante(estudiante: Estudiante):
 if estudiante.numero_control in estudiantes_db:
    raise HTTPException(status_code=409, detail="El número de control ya existe")
 estudiantes_db[estudiante.numero_control] = estudiante.model_dump()
 return {"mensaje": "Estudiante registrado", "estudiante": estudiante}

@app.put("/api/v1/estudiantes/{numero_control}")
def actualizar_estudiante(numero_control: str, estudiante: Estudiante):
 if numero_control not in estudiantes_db:
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")
 if estudiante.numero_control != numero_control:
    raise HTTPException(status_code=400, detail="El número de control de la ruta y del cuerpo debecoincidir")
 estudiantes_db[numero_control] = estudiante.model_dump()
 return {"mensaje": "Estudiante actualizado", "estudiante": estudiante}

@app.delete("/api/v1/estudiantes/{numero_control}", status_code=204)
def eliminar_estudiante(numero_control: str):
    if numero_control not in estudiantes_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    del estudiantes_db[numero_control]
    return


@app.get("/salud")
def salud():
 return {"estado": "correcto", "servicio": "api-escolar"}

from fastapi import FastAPI, HTTPException, Query

@app.get("/api/v1/estudiante-carrera/{carrera}")
def buscar_por_carrera(
    carrera: str,
    nombre: str | None = Query(default=None, min_length=2, description="Filtrar por coincidencia de nombre"),
    limite: int = Query(default=10, ge=1, le=100, description="Número máximo de resultados")
):
    resultado = [
        estudiante for estudiante in estudiantes_db.values()
        if estudiante["carrera"].lower() == carrera.lower()
    ]

    if nombre:
        resultado = [est for est in resultado if nombre.lower() in est["nombre"].lower()]

    resultado = resultado[:limite]

    if resultado:
        return resultado
    raise HTTPException(status_code=404, detail="No se encontraron estudiantes con los criterios especificados")



@app.get("/api/v2/estudiantes")
def listar_estudiantes_v2():
 return [
 {
 "numero_control": e["numero_control"],
 "nombre": e["nombre"],
 "programa_academico": e["carrera"]
 }
 for e in estudiantes_db.values()
 ]
