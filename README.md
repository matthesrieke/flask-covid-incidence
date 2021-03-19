# flask-covid-incidence

## dev server (docker-compose)

1. `docker-compose build`
1. `docker-compose up -d` (this also mounts the flask/server python files to the container)
1. Open browser: http://localhost:8080
1. OpenAPI UI: http://localhost:8080/v3/swagger-ui

Make changes, then restart:

1. `docker-compose restart flask`
