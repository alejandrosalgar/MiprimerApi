# Mi API con SQL Server y SQLAlchemy

Una API REST completa construida con FastAPI, SQLAlchemy y SQL Server que implementa los 4 métodos HTTP principales (GET, POST, PUT, DELETE) para la gestión de usuarios.

## Características

- **FastAPI**: Framework moderno y rápido para APIs con Python
- **SQLAlchemy**: ORM robusto para manejo de base de datos
- **SQL Server**: Base de datos empresarial de Microsoft
- **CRUD Completo**: Operaciones Create, Read, Update y Delete
- **Validación de Datos**: Con Pydantic para esquemas robustos
- **Documentación Automática**: Swagger UI integrado
- **Manejo de Errores**: Respuestas HTTP apropiadas
- **Soft Delete**: Opción de eliminar sin perder datos
- **CORS**: Configurado para desarrollo frontend
- **Migración Automática**: Base de datos se configura automáticamente

## Requisitos Previos

### Software Requerido
- **Python 3.8+**
- **SQL Server** (Express, Developer o Enterprise)
- **ODBC Driver 17 for SQL Server**

### Instalación de ODBC Driver
1. Descarga el [ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
2. Instala según tu sistema operativo
3. Verifica la instalación en el Administrador de Orígenes de Datos ODBC

## Instalación

### 1. Clonar o Descargar el Proyecto
```bash
git clone <url-del-repositorio>
cd MiApiSQLServer
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de la base de datos SQL Server
SQL_SERVER_CONNECTION_STRING=mssql+pyodbc://localhost/MiPrimerApiDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Desarrollo
DEBUG=true
RELOAD=true

# Logging
LOG_LEVEL=debug

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Seguridad
SECRET_KEY=clave_secreta_para_desarrollo_cambiar_en_produccion
TOKEN_EXPIRE_MINUTES=30
```

### 5. Configurar Base de Datos
1. Abre SQL Server Management Studio
2. Conéctate a tu instancia de SQL Server
3. Crea una nueva base de datos llamada `MiPrimerApiDB`
4. **IMPORTANTE**: Marca la casilla "Trust Server Certificate" en la conexión

```sql
-- Crear la base de datos
CREATE DATABASE MiPrimerApiDB;
```

## Ejecución

### Opción 1: Ejecución Directa (Recomendado)
```bash
# Desde la carpeta MiApiSQLServer
python main.py
```

### Opción 2: Con Uvicorn
```bash
# Desde la carpeta MiApiSQLServer
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 3: Con Uvicorn en Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Migración Automática de Base de Datos

### ¿Qué Hace la Migración?

Al iniciar la API, automáticamente se ejecuta:

1. **Conexión a SQL Server**
2. **Creación de tablas** (si no existen)
3. **Migración de esquemas**
4. **Inserción de datos de ejemplo**

### Tablas Creadas

#### Tabla `users`
```sql
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    full_name NVARCHAR(100),
    password NVARCHAR(255) NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    is_active BIT DEFAULT 1
);
```

#### Tabla `posts`
```sql
CREATE TABLE posts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    author_id INT NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    is_active BIT DEFAULT 1,
    FOREIGN KEY (author_id) REFERENCES users(id)
);
```

#### Tabla `comments`
```sql
CREATE TABLE comments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    content NVARCHAR(500) NOT NULL,
    post_id INT NOT NULL,
    author_id INT NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    is_active BIT DEFAULT 1,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);
```

### Datos de Ejemplo Insertados

- **Usuario admin**: `admin@ejemplo.com` / contraseña: `password`
- **Usuario ejemplo**: `usuario1@ejemplo.com` / contraseña: `password`

### Logs de Migración

Al iniciar la API verás:
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
Conexión a la base de datos exitosa
Tablas creadas exitosamente
Iniciando migración de la base de datos...
Migración completada exitosamente!
API iniciada correctamente
Base de datos conectada, tablas creadas y migración completada
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Endpoints Disponibles

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/users` | Obtener lista paginada de usuarios |
| `GET` | `/users/{id}` | Obtener usuario específico por ID |
| `POST` | `/users` | Crear nuevo usuario |
| `PUT` | `/users/{id}` | Actualizar usuario existente |
| `DELETE` | `/users/{id}` | Eliminar usuario (soft delete) |
| `DELETE` | `/users/{id}/hard` | Eliminar usuario permanentemente |

### Endpoints del Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `GET` | `/health` | Estado de salud de la API |
| `GET` | `/docs` | Documentación Swagger UI |

## Ejemplos de Uso

### Crear Usuario
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "juan_perez",
       "email": "juan@ejemplo.com",
       "full_name": "Juan Pérez",
       "password": "contraseña123"
     }'
```

### Obtener Usuarios
```bash
curl "http://localhost:8000/users?skip=0&limit=10"
```

### Actualizar Usuario
```bash
curl -X PUT "http://localhost:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{
       "full_name": "Juan Carlos Pérez"
     }'
```

### Eliminar Usuario
```bash
curl -X DELETE "http://localhost:8000/users/1"
```

## Estructura del Proyecto

```
MiApiSQLServer/
├── database/
│   ├── __init__.py
│   └── connection.py          # Configuración de SQLAlchemy, conexión y migración
├── models/
│   ├── __init__.py
│   └── schemas.py             # Modelos Pydantic y SQLAlchemy
├── endpoints/
│   ├── __init__.py
│   ├── get_users.py           # Endpoints GET (con ORDER BY para SQL Server)
│   ├── post_user.py           # Endpoint POST
│   ├── put_user.py            # Endpoint PUT
│   └── delete_user.py         # Endpoints DELETE
├── requirements.txt            # Dependencias del proyecto
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos a ignorar en Git
├── main.py                    # Aplicación principal FastAPI
└── README.md                  # Este archivo
```

## Solución de Problemas

### Error: "Login failed for user"
1. Verifica que SQL Server esté ejecutándose
2. Confirma que el string de conexión sea correcto
3. Asegúrate de que el usuario tenga permisos
4. Verifica que el ODBC Driver esté instalado

### Error: "Cannot open database"
1. Crea la base de datos `MiPrimerApiDB` en SQL Server
2. Verifica que el nombre de la base de datos sea correcto
3. Asegúrate de que el usuario tenga acceso a la base de datos

### Error: "Trust Server Certificate"
1. Marca la casilla "Trust Server Certificate" en SSMS
2. Agrega `TrustServerCertificate=yes` en tu string de conexión
3. O usa `Encrypt=no` para desarrollo local

### Error: "MSSQL requires an order_by when using OFFSET"
1. Este error ya está solucionado en el código
2. Las queries incluyen `ORDER BY` automáticamente
3. Si persiste, verifica que estés usando la versión actualizada

### Error: "Puerto en uso"
```bash
# Cambiar puerto en .env
PORT=8001

# O liberar el puerto 8000
netstat -ano | findstr :8000
taskkill /PID XXXX /F
```

### Error: "Not an executable object: 'SELECT 1'"
1. Este error ya está solucionado
2. La función `test_connection` usa `text("SELECT 1")` correctamente

## Testing

### Con Swagger UI
1. Ejecuta la API
2. Abre `http://localhost:8000/docs`
3. Usa la interfaz interactiva para probar endpoints

### Con Postman
1. Importa la colección de ejemplo
2. Configura las variables de entorno
3. Ejecuta las requests de prueba

### Con curl
```bash
# Health check
curl http://localhost:8000/health

# Obtener usuarios
curl http://localhost:8000/users

# Crear usuario
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"username":"test","email":"test@test.com","password":"test123"}'
```

## Despliegue en Producción

### Variables de Entorno de Producción
```env
# Configuración de producción
SQL_SERVER_CONNECTION_STRING=mssql+pyodbc://usuario:contraseña@servidor-produccion/base_de_datos?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
HOST=0.0.0.0
PORT=8000
WORKERS=4
DEBUG=false
RELOAD=false
```

### Comando de Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

### Con Docker (opcional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación de SQL Server](https://docs.microsoft.com/en-us/sql/)
- [Guía de ODBC Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)

## Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

---

**Desarrollado con amor usando FastAPI, SQLAlchemy y SQL Server**

## Changelog

### v1.0.0 - Versión Inicial
- API REST completa con FastAPI
- Conexión a SQL Server con SQLAlchemy
- CRUD completo para usuarios
- Migración automática de base de datos
- Documentación Swagger UI
- Manejo de errores robusto
- Soft delete implementado
- Datos de ejemplo incluidos
- Solución para OFFSET/LIMIT en SQL Server
