#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MYSQL_COMMAND="${MYSQL_COMMAND:-/opt/lampp/bin/mysql}"
MYSQL_HOST="${MYSQL_HOST:-localhost}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_ROOT_USER="${MYSQL_ROOT_USER:-root}"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-}"

if [[ ! -x "$MYSQL_COMMAND" ]]; then
    echo "Error: MySQL client is not executable: $MYSQL_COMMAND" >&2
    exit 1
fi

run_sql_script() {
    local script_name="$1"
    local script_path="${SCRIPT_DIRECTORY}/${script_name}"
    local password_arguments=()

    if [[ ! -f "$script_path" ]]; then
        echo "Error: SQL script not found: $script_path" >&2
        exit 1
    fi

    if [[ -n "$MYSQL_ROOT_PASSWORD" ]]; then
        password_arguments=("--password=${MYSQL_ROOT_PASSWORD}")
    fi
        echo "Running ${script_name}..."

    "$MYSQL_COMMAND" \
        --host="$MYSQL_HOST" \
        --port="$MYSQL_PORT" \
        --user="$MYSQL_ROOT_USER" \
        "${password_arguments[@]}" \
        < "$script_path"
}

echo "Starting database initialization..."

run_sql_script "drop_user.sql"
run_sql_script "drop_database.sql"
run_sql_script "create_database.sql"
run_sql_script "create_tables.sql"
run_sql_script "insert_data.sql"
run_sql_script "create_user.sql"

echo "Database initialization completed successfully."
