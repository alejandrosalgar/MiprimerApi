from database.connection import db
from models.schemas import Base
from sqlalchemy import text

def migrate_database():
    """Migra la base de datos usando SQL directo"""
    
    # Scripts SQL para crear las tablas
    create_users_table = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
    BEGIN
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(50) UNIQUE NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            full_name NVARCHAR(100),
            password NVARCHAR(255) NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1
        )
        
        -- Crear índices para mejor rendimiento
        CREATE INDEX IX_users_username ON users(username)
        CREATE INDEX IX_users_email ON users(email)
        CREATE INDEX IX_users_is_active ON users(is_active)
        
        PRINT 'Tabla users creada exitosamente'
    END
    ELSE
    BEGIN
        PRINT 'Tabla users ya existe'
    END
    """
    
    create_posts_table = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='posts' AND xtype='U')
    BEGIN
        CREATE TABLE posts (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(200) NOT NULL,
            content NVARCHAR(MAX) NOT NULL,
            author_id INT NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            updated_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
        
        CREATE INDEX IX_posts_author_id ON posts(author_id)
        CREATE INDEX IX_posts_created_at ON posts(created_at)
        
        PRINT 'Tabla posts creada exitosamente'
    END
    ELSE
    BEGIN
        PRINT 'Tabla posts ya existe'
    END
    """
    
    create_comments_table = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='comments' AND xtype='U')
    BEGIN
        CREATE TABLE comments (
            id INT IDENTITY(1,1) PRIMARY KEY,
            content NVARCHAR(500) NOT NULL,
            post_id INT NOT NULL,
            author_id INT NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
        
        CREATE INDEX IX_comments_post_id ON comments(post_id)
        CREATE INDEX IX_comments_author_id ON comments(author_id)
        
        PRINT 'Tabla comments creada exitosamente'
    END
    ELSE
    BEGIN
        PRINT 'Tabla comments ya existe'
    END
    """
    
    # Scripts para insertar datos de ejemplo
    insert_sample_users = """
    IF NOT EXISTS (SELECT * FROM users WHERE username = 'admin')
    BEGIN
        INSERT INTO users (username, email, full_name, password, is_active)
        VALUES 
            ('admin', 'admin@ejemplo.com', 'Administrador', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 1),
            ('usuario1', 'usuario1@ejemplo.com', 'Usuario Ejemplo', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 1)
        
        PRINT 'Usuarios de ejemplo insertados'
    END
    ELSE
    BEGIN
        PRINT 'Usuarios de ejemplo ya existen'
    END
    """
    
    try:
        print("Iniciando migración de la base de datos...")
        
        # Ejecutar scripts de creación de tablas
        db.execute_non_query(create_users_table)
        db.execute_non_query(create_posts_table)
        db.execute_non_query(create_comments_table)
        
        # Insertar datos de ejemplo
        db.execute_non_query(insert_sample_users)
        
        print("Migración completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        raise

if __name__ == "__main__":
    migrate_database()
