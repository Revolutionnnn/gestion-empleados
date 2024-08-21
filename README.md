Es necesario tener instalado docker para poder correr el proyecto

Primer paso construir el contenedor
docker compose up --build

Luego en caso de error con base de datos al construir el contenedor usar
docker compose up

Luego que ya este corriendo el contenedor correctamente la primera vez correr las migraciones
docker exec -it dev-empleados-backend python manage.py migrate

En caso que necesite correr nuevas migraciones usar el comando
docker exec -it dev-empleados-backend python manage.py makemigrations

Luego sera necesario crear un usuario administrador
docker exec -it dev-empleados-backend python manage.py createsuperuser

