

from src.services.cursor_pool import CursorPool


class MateriaService:
    
    def __init__(self):
        self.cursor_pool = CursorPool()

    def obtener_materias(self):
        with self.cursor_pool as cursor:
            sql = """
                select m.nombre, m.descripccion, s.nombre as semestre, s.id as semestre_id
                from materia m
                inner join semestre s on m.semestre_id = s.id;
            """
            cursor.execute(sql)
            return cursor.fetchall()
        
        
    def obtener_semestres(self):
        with self.cursor_pool as cursor:
            sql = "select * from semestre;"
            cursor.execute(sql)
            return cursor.fetchall()
        
    
    def obtener_eventos(self):
        with self.cursor_pool as cursor:
            sql = """
                select * from eventos;
            """
            cursor.execute(sql)
            return cursor.fetchall()
        
    def obtener_anuncios(self):
        with self.cursor_pool as cursor:
            sql = """
                SELECT * FROM anuncios
                ORDER BY 
                CASE LOWER(prioridad)
                    WHEN 'alta' THEN 1
                    WHEN 'media' THEN 2
                    WHEN 'baja' THEN 3
                END,
                fecha_publicacion DESC,
                hora_publicacion DESC;
            """
            cursor.execute(sql)
            return cursor.fetchall()
        
    def obtener_preguntas_frecuentes(self):
        with self.cursor_pool as cursor:
            sql = """
                select * from preguntas_frecuentes;
            """
            cursor.execute(sql)
            return cursor.fetchall()
