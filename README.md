# Instrucciones del taller:

## PROMPT 1:

estoy desarrollando un API para conectarme a una base de datos de PostgreSQL habilitada en Cloud SQL.
La base de datos se llama "panaderia" y tiene las tablas:
- productos (id, nombre, precio, descripcion)
- pedidos (id, cliente, total, fecha)
- pedido_productos(pedido_id, producto_id, cantidad)

Debo generar un backend sobre FastAPI con las siguientes funcionalidades:
- GET /productos - Lista de productos
- POST /pedido - Crear un pedido

Debo usar SQLALchemy para conectarme a Cloud SQL.

Además de generar la lógica, ayúdame con la creación del archivo requirements.txt

---
requirements.txt

fastapi
uvicorn
sqlalchemy
psycopg2-binary
gcp-sqlalchemy

---

### db.py

This file sets up the SQLAlchemy engine and session.

Explanation:

CLOUD_SQL_CONNECTION_NAME , DB_USER , DB_PASS , DB_NAME : These are environment variables or placeholder values for your Cloud SQL instance details. Crucially, for DB_PASS , you should use Google Secret Manager in a production environment instead of hardcoding it.
USE_CLOUD_SQL_CONNECTOR : This flag helps switch between using the Cloud SQL Python Connector (recommended for secure Cloud SQL connections) and a direct PostgreSQL connection.
Cloud SQL Python Connector ( google.cloud.sql.connector ) : This is the recommended way to connect to Cloud SQL from services like Cloud Run. It handles secure, encrypted connections. You need google-cloud-sql-connector and a database driver like pg8000 installed.
Direct Connection : Useful for local development with a local PostgreSQL instance.
Base = declarative_base() : The base class for your SQLAlchemy models.
engine : The SQLAlchemy engine, responsible for database interactions.
SessionLocal : A sessionmaker factory that will create new Session objects.
get_db() : A FastAPI dependency that provides a database session to endpoints and ensures it's closed after the request.


## models.py
This file defines the SQLAlchemy ORM models corresponding to your database tables.

Explanation:

Base : Imported from database.py .
__tablename__ : Specifies the table name in the database.
Column : Defines a database column with its type and constraints (e.g., primary_key=True , index=True , nullable=True ).
ForeignKey : Establishes relationships between tables.
relationship : Defines the ORM relationships between models, allowing you to access related objects (e.g., pedido.pedidos_productos to get all products in a specific order).
func.now() : Automatically sets the fecha column to the current timestamp when a Pedido is created.

## schemas.py
This file defines Pydantic models for data validation and serialization. These are used by FastAPI for request body validation and response serialization.

Explanation:

BaseModel : Pydantic's base class for creating schemas.
Optional : Indicates that a field can be None .
List : Used for lists of items (e.g., items in PedidoCreate ).
Config.from_attributes = True : Tells Pydantic to read data from SQLAlchemy ORM models (attributes) instead of just dictionary keys. This replaces orm_mode = True from older Pydantic versions.
We define separate schemas for creation ( ProductoCreate , PedidoCreate ) and for reading data ( Producto , Pedido ). This allows for different validation rules or fields depending on the operation.


## main.py
This is the main FastAPI application file.

Explanation:

FastAPI() : Initializes the FastAPI application.
@app.on_event("startup") : This decorator makes sure the create_all method is called when the application starts. models.Base.metadata.create_all(bind=database.engine) will create all tables defined in models.py if they don't already exist in your database. For production, you should use a proper database migration tool like Alembic.
get_db = database.get_db : Assigns the get_db dependency to be used in endpoints.
@app.get("/productos", response_model=List[schemas.Producto]) :
Defines a GET endpoint at /productos .
response_model : Specifies the Pydantic schema for the response, ensuring the output matches List[schemas.Producto] .
skip and limit : Optional query parameters for pagination.
db: Session = Depends(get_db) : Injects a database session into the endpoint function.
db.query(models.Producto).offset(skip).limit(limit).all() : SQLAlchemy query to fetch products.
@app.post("/pedidos", response_model=schemas.Pedido, status_code=status.HTTP_201_CREATED) :
Defines a POST endpoint at /pedidos .
response_model : schemas.Pedido for the created order.
status_code : Sets the HTTP status code for successful creation to 201.
pedido_data: schemas.PedidoCreate : FastAPI automatically validates the request body against schemas.PedidoCreate .
The logic iterates through pedido_data.items , fetches product details to calculate the total, creates a Pedido object, and then creates PedidoProducto entries to link the order and its products.
db.add() , db.commit() , db.refresh() : Standard SQLAlchemy operations for persisting and refreshing objects.
Error handling for Product not found .



--- 
How to run local to test

pip install -r requirements.txt

For Cloud SQL Python Connector (recommended even for local testing if you want to connect to a real Cloud SQL instance):

export CLOUD_SQL_CONNECTION_NAME="your-project-id:your-region:your-instance-name"
export DB_USER="your-db-user"
export DB_PASS="your-db-password"
export DB_NAME="panaderia"
export USE_CLOUD_SQL_CONNECTOR="True"


export DB_USER="postgres" # Or your local user
export DB_PASS="your-local-db-password"
export DB_NAME="panaderia"
export USE_CLOUD_SQL_CONNECTOR="False"


uvicorn main:app --reload



---

When deploying to Cloud Run, ensure you configure the following:

Environment Variables : Set CLOUD_SQL_CONNECTION_NAME , DB_USER , DB_NAME in your Cloud Run service settings. For DB_PASS , use Secret Manager and mount it as an environment variable or retrieve it programmatically.
Cloud SQL Connection : In the Cloud Run service settings, link your Cloud SQL instance under "Connections." This enables the Cloud SQL Proxy functionality, allowing your service to connect securely to Cloud SQL using the Python Connector.
IAM Permissions : The Service Account associated with your Cloud Run service needs the Cloud SQL Client role to connect to the database. If using Secret Manager for the password, it also needs the Secret Manager Secret Accessor role.
Dockerfile : You'll need a Dockerfile to containerize your FastAPI application for Cloud Run.



# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app listens on
EXPOSE 8080

# Run the uvicorn server with 4 workers, binding to 0.0.0.0:8080
# Use gunicorn in production for process management
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]



---
# Prompt 2

AL instalar requirements,txt entregado anteriormente, se me generó este error: ERROR: Could not find a version that satisfies the requirement gcp-sqlalchemy (from versions: none) ERROR: No matching distribution found for gcp-sqlalchemy Qué debo hacer? ¿Cómo impacta mi proyecto?

fastapi
uvicorn
sqlalchemy
psycopg2-binary
google-cloud-sqlalchemy


# Comando

gcloud run deploy panaderia --source . --set-env-vars DB_USER=panadero,DB_PASS=password,DB_NAME=panaderia