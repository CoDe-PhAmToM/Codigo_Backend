
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from urllib.parse import urlparse
import threading
import os

class Database:
    load_dotenv()
    __url = urlparse(os.getenv("DATABASE_URL")) 
    _DATABASE = __url.path[1:]
    _USERNAME = __url.username
    _PASSWORD = __url.password
    _HOST = __url.hostname
    _PORT = __url.port
    _pool = None
    _minconn = 1
    _maxconn = 5

    @classmethod
    def obtener_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    cls._minconn,
                    cls._maxconn,
                    host=cls._HOST,
                    port=cls._PORT,
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    database=cls._DATABASE,
                    cursor_factory=RealDictCursor)
                print("✅ Pool de conexiones creado.")
            except Exception as e:
                print(f"❌ Error al crear el pool de conexiones: {e}")
                raise e
        return cls._pool
    
    @classmethod
    def obtener_conexion(cls):
        conexion = cls.obtener_pool().getconn()
        return conexion
    
    @classmethod
    def liberar_conexion(cls, conexion):
        cls.obtener_pool().putconn(conexion)
    
    @classmethod
    def cerrar_pool(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            print("✅ Pool de conexiones cerrado.")












# class DataBase:
#     __pool = None

#     @classmethod
#     def initialize(cls):
#         if cls.__pool is None:
#             cls.__pool = pool.SimpleConnectionPool(
#                 minconn=1,
#                 maxconn=10,
#                 host=os.getenv("DB_HOST", "localhost"),
#                 database=os.getenv("DB_NAME", "educacion"),
#                 user=os.getenv("DB_USER", "postgres"),
#                 password=os.getenv("DB_PASSWORD", "melapelas123"),
#                 cursor_factory=RealDictCursor
#             )
#             print("✅ Pool de conexiones creado.")

#     def __init__(self):
#         if self.__pool is None:
#             raise Exception("❌ Pool de conexiones no inicializado.")
#         self.conn = self.__pool.getconn()
#         self.cursor = self.conn.cursor()

#     def __enter__(self):
#         return self.cursor

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if exc_val:
#             self.conn.rollback()
#         else:
#             self.conn.commit()
#         self.cursor.close()
#         self.__pool.putconn(self.conn)

















# # import psycopg2
# # from psycopg2.extras import RealDictCursor

# # class DataBase:
    
# #     def __init__(self):
# #         self.conn = psycopg2.connect(
# #             host="localhost",
# #             database="educacion",
# #             user="postgres",
# #             password="melapelas123",
        

# #         )
# #         print("Conectado a la base de datos")
        
# #     def __enter__(self):
# #         self.conn.cursor_factory = RealDictCursor
# #         self.cursor = self.conn.cursor()
# #         return self.cursor
    
# #     def __exit__(self, exc_type, exc_val, exc_tb):
# #         if exc_val is not None:
# #             self.conn.rollback()
# #         else:
# #             self.conn.commit()
# #         self.cursor.close()
# #         self.conn.close()
# #         print("Desconectado de la base de datos")