from src.services.cursor_pool import CursorPool

class IngeniaRedService:

    def __init__(self):
        self.cursor_pool = CursorPool()

    def obtener_materias(self):
        with self.cursor_pool as cursor:
            sql = """
                SELECT 
                    s.subject_id AS id, 
                    s.name AS nombre, 
                    s.description AS descripcion, 
                    sem.name AS semestre, 
                    sem.semester_id AS semestre_id
                FROM subjects s
                INNER JOIN semesters sem ON s.semester_id = sem.semester_id;
            """
            cursor.execute(sql)
            return cursor.fetchall()
        
    def obtener_semestres(self):
        with self.cursor_pool as cursor:
            sql = "SELECT * FROM semesters;"
            print(sql)
            cursor.execute(sql)
            return cursor.fetchall()
        
    def obtener_eventos(self):
        with self.cursor_pool as cursor:
            sql = """
                SELECT event_id AS id,
                       title AS titulo,
                       description AS descripcion,
                       start_time AS fecha_inicio,
                       end_time AS fecha_fin,
                       location AS ubicacion,
                       event_type AS tipo_evento,
                       is_public AS es_publico
                FROM events;
            """
            print(sql)
            cursor.execute(sql)
            return cursor.fetchall()
        
    def obtener_anuncios(self):
        with self.cursor_pool as cursor:
            sql = """
                SELECT announcement_id AS id,
                       title AS titulo,
                       content AS contenido,
                       publish_date AS fecha_publicacion,
                       priority AS prioridad,
                       target AS objetivo
                FROM announcements
                ORDER BY 
                priority,
                publish_date DESC;
            """
            print(sql)
            cursor.execute(sql)
            return cursor.fetchall()
        
    def obtener_preguntas_frecuentes(self):
        with self.cursor_pool as cursor:
            sql = """
                SELECT faq_id AS id,
                       question AS pregunta,
                       answer AS respuesta,
                       category AS categoria,
                       is_featured AS destacado
                FROM faqs
                ORDER BY is_featured DESC;
            """
            cursor.execute(sql)
            return cursor.fetchall()

    def obtener_contenidos_academicos(self, filtros=None):
        """
        Obtiene contenidos académicos con filtros opcionales de manera simplificada
        
        Args:
            filtros (dict): Diccionario con filtros opcionales. Ejemplo:
                {
                    'semestre_id': 1,
                    'materia_id': 5,
                    'busqueda': 'matemáticas',
                    'tipo_contenido': 'pdf',
                    'limite': 10,
                    'orden': 'fecha'  # 'fecha' o 'descargas'
                }
        
        Returns:
            list: Lista de diccionarios con los contenidos académicos
        """
        with self.cursor_pool as cursor:
            # Consulta base
            sql = """
                SELECT 
                    ac.content_id AS id,
                    ac.title AS titulo,
                    ac.description AS descripcion,
                    ac.file_path AS ruta_archivo,
                    ac.upload_date AS fecha_subida,
                    ac.downloads AS descargas,
                    u.first_name || ' ' || u.last_name AS autor,
                    ct.name AS tipo_contenido,
                    s.name AS materia,
                    sem.name AS semestre,
                    s.subject_id AS materia_id,
                    sem.semester_id AS semestre_id
                FROM 
                    academic_contents ac
                JOIN 
                    users u ON ac.user_id = u.user_id
                JOIN 
                    content_types ct ON ac.type_id = ct.type_id
                JOIN
                    subjects s ON ac.subject_id = s.subject_id
                JOIN
                    semesters sem ON s.semester_id = sem.semester_id
                WHERE 
                    ac.is_approved = TRUE
                    AND ac.visibility = 'public'
            """
            
            # Parámetros para la consulta
            params = []
            
            # Aplicar filtros dinámicos
            if filtros:
                # Filtro por semestre
                if 'semestre_id' in filtros:
                    sql += " AND sem.semester_id = %s"
                    params.append(filtros['semestre_id'])
                
                # Filtro por materia
                if 'materia_id' in filtros:
                    sql += " AND s.subject_id = %s"
                    params.append(filtros['materia_id'])
                
                # Filtro por búsqueda de texto
                if 'busqueda' in filtros:
                    sql += " AND (ac.title ILIKE %s OR ac.description ILIKE %s OR s.name ILIKE %s)"
                    params.extend([
                        f"%{filtros['busqueda']}%", 
                        f"%{filtros['busqueda']}%",
                        f"%{filtros['busqueda']}%"
                    ])
                
                # Filtro por tipo de contenido
                if 'tipo_contenido' in filtros:
                    sql += " AND ct.name = %s"
                    params.append(filtros['tipo_contenido'])
            
            # Ordenamiento
            if filtros and filtros.get('orden') == 'descargas':
                sql += " ORDER BY ac.downloads DESC"
            else:
                sql += " ORDER BY ac.upload_date DESC"  # Orden por defecto
            
            # Límite de resultados
            if filtros and 'limite' in filtros:
                sql += " LIMIT %s"
                params.append(filtros['limite'])
            
            cursor.execute(sql, params)
            return cursor.fetchall()

    def obtener_documentos_por_materia(self, subject_id):
        # Este método ahora puede ser reemplazado por:
        # obtener_contenidos_academicos({'materia_id': subject_id})
        with self.cursor_pool as cursor:
            sql = """
                SELECT 
                    ac.content_id AS id,
                    ac.title AS titulo,
                    ac.description AS descripcion,
                    ac.file_path AS ruta_archivo,
                    ac.upload_date AS fecha_subida,
                    ac.downloads AS descargas,
                    u.first_name || ' ' || u.last_name AS autor,
                    ct.name AS tipo_contenido,
                    s.subject_id AS materia_id, 
                    sem.semester_id AS semestre_id  
                FROM 
                    academic_contents ac
                JOIN 
                    users u ON ac.user_id = u.user_id
                JOIN 
                    content_types ct ON ac.type_id = ct.type_id
                JOIN
                    subjects s ON ac.subject_id = s.subject_id
                JOIN
                    semesters sem ON s.semester_id = sem.semester_id
                WHERE 
                    ac.subject_id = %s
                    AND ac.is_approved = TRUE
                    AND ac.visibility = 'public'
                ORDER BY 
                    ac.upload_date DESC;
            """
            cursor.execute(sql, (subject_id,))
            return cursor.fetchall()

    def incrementar_descargas(self, content_id):
        with self.cursor_pool as cursor:
            sql = """
                UPDATE academic_contents
                SET downloads = downloads + 1
                WHERE content_id = %s
                RETURNING downloads;
            """
            cursor.execute(sql, (content_id,))
            return cursor.fetchone()[0]
    
    def guardar_documento(self, title, description, file_path, subject_id, user_id, type_id=1):
        with self.cursor_pool as cursor:
            sql = """
                INSERT INTO academic_contents 
                (subject_id, user_id, type_id, title, description, file_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING content_id;
            """
            cursor.execute(sql, (subject_id, user_id, type_id, title, description, file_path))
            return cursor.fetchone()[0]













# from src.services.cursor_pool import CursorPool

# class IngeniaRedService:

#     def __init__(self):
#         self.cursor_pool = CursorPool()

#     def obtener_materias(self):
#         with self.cursor_pool as cursor:
#             sql = """
#                 select m.nombre, m.descripccion, s.nombre as semestre, s.id as semestre_id
#                 from materia m
#                 inner join semestre s on m.semestre_id = s.id;
#             """
#             cursor.execute(sql)
#             return cursor.fetchall()
        
        
#     def obtener_semestres(self):
#         with self.cursor_pool as cursor:
#             sql = "select * from semestre;"
#             cursor.execute(sql)
#             return cursor.fetchall()
        
    
#     def obtener_eventos(self):
#         with self.cursor_pool as cursor:
#             sql = """
#                 select * from eventos;
#             """
#             cursor.execute(sql)
#             return cursor.fetchall()
        
#     def obtener_anuncios(self):
#         with self.cursor_pool as cursor:
#             sql = """
#                 SELECT * FROM anuncios
#                 ORDER BY 
#                 CASE LOWER(prioridad)
#                     WHEN 'alta' THEN 1
#                     WHEN 'media' THEN 2
#                     WHEN 'baja' THEN 3
#                 END,
#                 fecha_publicacion DESC,
#                 hora_publicacion DESC;
#             """
#             cursor.execute(sql)
#             return cursor.fetchall()
        
#     def obtener_preguntas_frecuentes(self):
#         with self.cursor_pool as cursor:
#             sql = """
#                 select * from preguntas_frecuentes;
#             """
#             cursor.execute(sql)
#             return cursor.fetchall()
