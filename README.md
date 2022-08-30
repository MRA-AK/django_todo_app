# django_todo_app
Class base view django todo app

## How To Use
1. Install docker and docker compose.
2. Clone the repository.
3. Run the docker compose: `docker compose up --build` 
4. Create database: `docker exec backend python manage.py migrate`
5. Open your browser and go to http://localhost:8000/.

## API
API root endpoint: http://localhost:8000/api/v1/task/
#### API Docs:
- DRF built-in documentation: http://localhost:8000/drf-docs/
- Swagger documentation: http://localhost:8000/swagger/
- Redoc documentation: http://localhost:8000/redoc/
- Export swagger in json format: http://localhost:8000/swagger/output.json/

## Create dummy data
For creating five dummy tasks:
run `docker-compose exec backend sh -c "python manage.py insert_data"`
