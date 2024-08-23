# Proyecto Gestion de ingresos

Este proyecto requiere tener **Docker** instalado para su ejecución.

## Instrucciones para Configuración y Ejecución

### 1. Decargar el proyecto
Luego de descargar el proyecto sera necesario ingresar a la carpeta donde se encuentre el proyecto

### 2. Construcción del Contenedor
Primero, construye el contenedor con el siguiente comando:

docker compose up --build
En caso de que genere error al crear el contenedor sera necesario apagar el contenedor
Y de nuevo usar
docker compose up

### 3. Realizar migraciones
docker exec -it dev-empleados-backend python manage.py migrate

### 4. Crear usuarios administrador
docker exec -it dev-empleados-backend python manage.py createsuperuser

#### 5. Comandos adicionales
Crear migraciones
docker exec -it dev-empleados-backend python manage.py makemigrations

Levantar contenedor
docker compose up

####  Puertos de la app
Frontend http://127.0.0.1:9000/
Backend http://127.0.0.1:8000/
Base de datos 5435
