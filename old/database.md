




docker run --name local-postgres-db \
    -e POSTGRES_USER=panadero \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=panaderia \
    -p 127.0.0.1:5432:5432 \
    -d postgres





export CLOUD_SQL_CONNECTION_NAME="your-project-id:your-region:your-instance-name"
export DB_USER="panadero"
export DB_PASS="password"
export DB_NAME="panaderia"
export DB_HOST="127.0.0.1"
export DB_PORT="5432"

export USE_CLOUD_SQL_CONNECTOR="True"

export DB_USER="myuser"
export DB_PASS="mypassword"
export DB_NAME="tabs_vs_spaces_db"
