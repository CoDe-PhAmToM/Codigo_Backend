from src.services.database import Database


class CursorPool():
    def __init__(self):
        self.conexion = None
        self.cursor = None
    
    def __enter__(self):
        self.conexion = Database.obtener_conexion()
        self.cursor = self.conexion.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.conexion.rollback()
        else:
            self.conexion.commit()
        self.conexion.close()
        Database.liberar_conexion(self.conexion)