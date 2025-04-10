#!/bin/sh
set -e

# Function to check if database is ready
check_db_connection() {
  python -c "import MySQLdb; MySQLdb.connect(host='$DB_HOST', user='$DB_USER', password='$DB_PASS', database='$DB_NAME')" 2>/dev/null
  return $?
}

echo "Waiting for database to be ready..."
RETRIES=30
RETRY_INTERVAL=2

for i in $(seq 1 $RETRIES); do
  if check_db_connection; then
    echo "Database is ready!"
    exit 0
  fi
  
  echo "Database not ready yet (attempt $i of $RETRIES)... waiting $RETRY_INTERVAL seconds"
  sleep $RETRY_INTERVAL
done

echo "Failed to connect to database after $RETRIES attempts"
exit 1