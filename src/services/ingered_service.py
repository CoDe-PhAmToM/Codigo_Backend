from src.services.cursor_pool import CursorPool

class IngeniaRedService:

    def __init__(self):
        self.cursor_pool = CursorPool()

    def obtener_materias(self):
        with self.cursor_pool as cursor:
            sql = """
                SELECT s.name AS nombre, 
                       s.description AS descripcion, 
                       sem.name AS semestre, 
                       sem.semester_id AS semestre_id
                FROM subjects s
                INNER JOIN semesters sem ON s.semester_id = sem.semester_id;
            """
            print(sql)
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
                FROM faqs;
            """
            cursor.execute(sql)
            return cursor.fetchall()















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
