from flask import Flask, request, jsonify, render_template
import pymysql
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/sql_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload_sql.html')

def execute_sql(host, user, password, port, sql_file_path):
    results = []
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection:
            with connection.cursor() as cursor:
                with open(sql_file_path, 'r') as file:
                    sql_commands = file.read().split(';')
                    for command in sql_commands:
                        if command.strip():
                            cursor.execute(command)
                            results.append(cursor.fetchall())
            connection.commit()
    except Exception as e:
        results = {"error": str(e)}
    return results

@app.route('/run_sql', methods=['POST'])
def run_sql():
    try:
        host = request.form['host']
        user = request.form['username']
        password = request.form['password']
        port = int(request.form['port'])

        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        results = execute_sql(host, user, password, port, file_path)
        os.remove(file_path)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/run_single_query', methods=['POST'])
def run_single_query():
    try:
        # Retrieve database credentials and the query from the request
        host = request.form['host']
        user = request.form['username']
        password = request.form['password']
        port = int(request.form['port'])
        query = request.form['query']

        # Connect to MariaDB and execute the single query
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            cursorclass=pymysql.cursors.DictCursor
        )
        results = []
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
            connection.commit()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
