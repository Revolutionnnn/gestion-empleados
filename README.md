# Proyecto Django con Docker

Este proyecto requiere tener **Docker** instalado para su ejecución.

## Instrucciones para Configuración y Ejecución

### 1. Construcción del Contenedor

Primero, construye el contenedor con el siguiente comando:

docker compose up --build

### 2. Realizar migraciones
docker exec -it dev-empleados-backend python manage.py migrate

### 3. Crear usuarios administrador
docker exec -it dev-empleados-backend python manage.py createsuperuser

#### 4. Comandos adicionales
Crear migraciones
docker exec -it dev-empleados-backend python manage.py makemigrations

Levantar contenedor
docker compose up
