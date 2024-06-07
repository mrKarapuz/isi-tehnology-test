# Text task

### Technologies
 * Django
 * Nginx - proxy
 * SQLite - database
 * Redis - Cache
 * Poetry - requirements

### Run local

1. Configure .env
2. Run commands
```
python /app/manage.py collectstatic --noinput && python /app/manage.py makemigrations && python /app/manage.py migrate && python /app/manage.py runserver 0.0.0.0:8000
```

### Quick Start

1. Copy docker-compose.yml to server with config files
   * config/docker/nginx.dockerfile
   * config/nginx/django.conf
   * config/nginx/uwsgi_paras
   * config/redis/redis.conf
   * config/ssl/cert.pem
   * config/ssl/key.pem
   * config/uwsgi/uwsgi.ini

2. Configure .docker.env

3. Create network
```bash
docker network create isi_test_network
```

4. Run containers
```bash
docker-compose up --build
```

5. Migrate
```bash
docker compose exec django python manage.py migrate
```

6. Collectstatic
```bash
docker compose exec django python manage.py collectstatic --clear
```

7. Createsuperuser
```bash
docker compose exec django python manage.py createsuperuser
```
