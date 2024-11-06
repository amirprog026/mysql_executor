
# MariaDB SQL Execution Service
This service allows users to run SQL commands on a remote MariaDB database using either an uploaded .sql file or a single SQL query.

## Features
- Execute multiple SQL commands from a .sql file
- Run a single SQL query
- Display query results in JSON format


## Structure
```
├── templates/
│   └── upload_sql.html | single_sql.html     # HTML form for executing SQL commands
├── app.py                  # Main Flask application file
└── README.md               # Project README with usage instructions

```

## Requirements

- Python 3.7+
- Flask
- PyMySQL(for MariaDB connection)
## Endpoints
```
1. GET /
Renders the HTML interface for SQL file upload and single query execution.
2. POST /run_sql
Executes SQL commands from an uploaded .sql file on the remote MariaDB.
Parameters:
host: Database host (e.g., localhost)
username: Database username
password: Database password
port: Database port (default is 3306)
file: The .sql file containing SQL commands
Response: JSON object with query results or error messag
```
## Example
Query by file
```
curl -X POST -F "host=your_mariadb_host" \
-F "username=your_user" \
-F "password=your_password" \
-F "port=3306" \
-F "file=@path_to_your_file.sql" \
http://127.0.0.1:5000/run_sql
```

Single Query
```
curl -X POST -F "host=your_mariadb_host" \
-F "username=your_user" \
-F "password=your_password" \
-F "port=3306" \
-F "query=SELECT * FROM your_table" \
http://127.0.0.1:5000/run_single_query
```
