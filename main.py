import time
import fastapi
import fastapi.middleware.cors
from fastapi import UploadFile, File, Form, Query
from typing import List, Optional
import os
from src.services.ingered_service import IngeniaRedService
from fastapi import Query, HTTPException

app = fastapi.FastAPI()

# Configuración CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://upea-sistemas.vercel.app"
]

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

servicios_ingred = IngeniaRedService()

# Endpoints existentes (se mantienen igual)
@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API con FastAPI"}

@app.get("/materias/obtener")
async def get_materias():
    materias = servicios_ingred.obtener_materias()
    return materias

@app.get("/semestres/obtener")
async def get_semestres():
    semestres = servicios_ingred.obtener_semestres()
    return semestres

@app.get("/eventos/obtener")
async def get_eventos():
    eventos = servicios_ingred.obtener_eventos()
    return eventos

@app.get("/anuncios/obtener")
async def get_anuncios():
    anuncios = servicios_ingred.obtener_anuncios()
    return anuncios

@app.get("/preguntas_frecuentes/obtener")
async def get_preguntas_frecuentes():
    faqs = servicios_ingred.obtener_preguntas_frecuentes()
    return faqs

# Nuevos endpoints para documentos académicos
@app.get("/documentos/materia/{subject_id}")
async def get_documentos_por_materia(subject_id: int):
    documentos = servicios_ingred.obtener_documentos_por_materia(subject_id)
    return {"documentos": documentos}

@app.get("/documentos/filtrados")
async def get_documentos_filtrados(
    semestre_id: Optional[int] = Query(None),
    materia_id: Optional[int] = Query(None),
    termino_busqueda: Optional[str] = Query(None)
):
    documentos = servicios_ingred.obtener_documentos_filtrados(
        semester_id=semestre_id,
        subject_id=materia_id,
        search_term=termino_busqueda
    )
    return {"documentos": documentos}

@app.post("/documentos/{content_id}/descargar")
async def registrar_descarga(content_id: int):
    new_count = servicios_ingred.incrementar_descargas(content_id)
    return {"descargas": new_count}

# Endpoint para subir archivos (mejorado)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    description: str = Form(None)
):
    for file in files:
        contents = await file.read()
        # Aquí guardas o procesas el archivo
        with open(f"./{UPLOAD_DIR}/{file.filename}", "wb") as f:
            f.write(contents)
    return {"message": "Archivos recibidos"}


# @app.post("/upload")
# async def upload_files(
#     files: List[UploadFile] = File(...),
#     description: str = Form(default="Sin descripción"),
#     subject_id: int = Form(...),
#     user_id: int = Form(...),
#     type_id: int = Form(default=1)  # 1 puede ser el ID por defecto para "Documento genérico"
# ):
#     results = []
    
#     for file in files:
#         # Validación básica del tipo de archivo
#         file_extension = os.path.splitext(file.filename)[1].lower()
#         if file_extension not in ['.pdf', '.docx', '.pptx', '.txt']:
#             results.append({
#                 "filename": file.filename,
#                 "error": "Tipo de archivo no permitido",
#                 "status": "failed"
#             })
#             continue

#         # Crear nombre único para el archivo
#         unique_filename = f"{user_id}_{int(time.time())}_{file.filename}"
#         file_path = os.path.join(UPLOAD_DIR, unique_filename)

#         try:
#             # Guardar archivo físicamente
#             contents = await file.read()
#             with open(file_path, "wb") as f:
#                 f.write(contents)

#             # Guardar metadatos en la base de datos
#             content_id = servicios_ingred.guardar_documento(
#                 title=file.filename,
#                 description=description,
#                 file_path=file_path,  # o unique_filename si prefieres
#                 subject_id=subject_id,
#                 user_id=user_id,
#                 type_id=type_id
#             )

#             results.append({
#                 "filename": file.filename,
#                 "saved_path": file_path,
#                 "content_id": content_id,
#                 "status": "success"
#             })

#         except Exception as e:
#             # Si hay error, eliminar el archivo si se creó
#             if os.path.exists(file_path):
#                 os.remove(file_path)
                
#             results.append({
#                 "filename": file.filename,
#                 "error": str(e),
#                 "status": "failed"
#             })
#     print(results)
#     return {
#         "message": "Procesamiento completado",
#         "results": results,
#         "summary": {
#             "success": len([r for r in results if r["status"] == "success"]),
#             "failed": len([r for r in results if r["status"] == "failed"])
#         }
#     }


@app.get("/contenidos/academicos")
async def obtener_contenidos_academicos(
    semestre_id: int = Query(None, description="Filtrar por ID de semestre"),
    materia_id: int = Query(None, description="Filtrar por ID de materia"),
    tipo_contenido: str = Query(None, description="Filtrar por tipo de contenido"),
    busqueda: str = Query(None, description="Búsqueda textual en título, descripción o materia"),
    orden: str = Query('fecha', description="Criterio de ordenamiento (fecha o descargas)"),
    limite: int = Query(None, description="Límite de resultados")
):
    try:
        # Construimos el diccionario de filtros
        filtros = {
            'semestre_id': semestre_id,
            'materia_id': materia_id,
            'tipo_contenido': tipo_contenido,
            'busqueda': busqueda,
            'orden': orden,
            'limite': limite
        }
        
        # Eliminamos filtros None para que el servicio use sus valores por defecto
        filtros = {k: v for k, v in filtros.items() if v is not None}
        
        contenidos = servicios_ingred.obtener_contenidos_academicos(filtros)
        
        return {
            "success": True,
            "data": contenidos,
            "count": len(contenidos)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener contenidos académicos: {str(e)}"
        )








# import fastapi, fastapi.middleware.cors
# from fastapi.params import File
# from fastapi import UploadFile, File, Form
# import os
# from typing import List
# from src.services.ingered_service import IngeniaRedService


# app = fastapi.FastAPI()
# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     #"https://codigo-frontend-black.vercel.app",
#     "https://upea-sistemas.vercel.app"
# ]

# app.add_middleware(
#     fastapi.middleware.cors.CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]  # Añade esta línea
# )

# servicios_ingred = IngeniaRedService()

# @app.get("/")
# def read_root():
#     return {"message": "Bienvenido a mi API con FastAPI"}

# @app.get("/materias/obtener")
# async def get_materias():
    
#     materias = servicios_ingred.obtener_materias()

#     return materias

# @app.get("/semestres/obtener")
# async def get_semestres():
    
#     semestres = servicios_ingred.obtener_semestres()

#     return semestres

# @app.get("/eventos/obtener")
# async def get_eventos():
    
#     eventos = servicios_ingred.obtener_eventos()

#     return eventos

# @app.get("/anuncios/obtener")
# async def get_anuncios():
    
#     anuncios = servicios_ingred.obtener_anuncios()

#     return anuncios

# @app.get("/preguntas_frecuentes/obtener")
# async def get_preguntas_frecuentes():
    
#     faqs = servicios_ingred.obtener_preguntas_frecuentes()

#     return faqs

# @app.post("/upload")
# async def upload_files(
#     files: List[UploadFile] = File(...),
#     description: str = Form(None)
# ):
#     for file in files:
#         contents = await file.read()
#         # Aquí guardas o procesas el archivo
#         with open(f"./uploads/{file.filename}", "wb") as f:
#             f.write(contents)
#     return {"message": "Archivos recibidos"}




# @app.post("/contenido/upload")
# async def subir_contenido(
#     contenido: str = Form(...),
#     materia: str = Form(...),
#     semestre: str = Form(...),
#     archivo: UploadFile = File(...)
# ):
#     carpeta_destino = "archivos_subidos"
#     os.makedirs(carpeta_destino, exist_ok=True)

#     ruta_archivo = os.path.join(carpeta_destino, archivo.filename)
#     with open(ruta_archivo, "wb") as buffer:
#         shutil.copyfileobj(archivo.file, buffer)

#     return JSONResponse(content={
#         "mensaje": "Contenido subido exitosamente",
#         "archivo": archivo.filename,
#         "materia": materia,
#         "semestre": semestre,
#         "contenido": contenido
#     })

