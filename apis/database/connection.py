import pyodbc
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection_string = os.getenv('SQL_SERVER_CONNECTION_STRING')
        if not self.connection_string:
            # String de conexión por defecto - modifica según tu configuración
            self.connection_string = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=MiPrimerApiDB;"
                "UID=sa;"
                "PWD=TuPassword123;"
                "TrustServerCertificate=yes;"
            )
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        try:
            connection = pyodbc.connect(self.connection_string)
            return connection
        except Exception as e:
            print(f"Error conectando a la base de datos: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None):
        """Ejecuta una consulta SELECT"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            raise
    
    def execute_non_query(self, query: str, params: tuple = None):
        """Ejecuta INSERT, UPDATE, DELETE"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error ejecutando non-query: {e}")
            raise
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        create_users_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(50) UNIQUE NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            full_name NVARCHAR(100),
            password NVARCHAR(255) NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1
        )
        """
        
        try:
            self.execute_non_query(create_users_table)
            print("Tablas creadas exitosamente")
        except Exception as e:
            print(f"Error creando tablas: {e}")

# Instancia global de la conexión
db = DatabaseConnection()
