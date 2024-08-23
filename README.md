# Proyecto Gestion de ingresos

Este proyecto requiere tener **Docker** instalado para su ejecución.

## Instrucciones para Configuración y Ejecución

### 1. Decargar el proyecto
Luego de descargar el proyecto sera necesario ingresar a la carpeta donde se encuentre el proyecto

### 2. Construcción del Contenedor
Primero, construye el contenedor con el siguiente comando:

docker compose up --build

### 3. Realizar migraciones
docker exec -it dev-empleados-backend python manage.py migrate

### 4. Crear usuarios administrador
docker exec -it dev-empleados-backend python manage.py createsuperuser

#### 5. Comandos adicionales
Crear migraciones
docker exec -it dev-empleados-backend python manage.py makemigrations

Levantar contenedor
docker compose up
