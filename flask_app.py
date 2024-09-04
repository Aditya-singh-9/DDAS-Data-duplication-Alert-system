from flask import Flask, request, jsonify
import boto3
import hashlib
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database (replace with your DB details)
def connect_db():
    try:
        return mysql.connector.connect(
            host="your-aws-rds-endpoint",
            user="your-db-username",
            password="your-db-password",
            database="ddas"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Compute the SHA-256 hash of the file content
def compute_file_hash(file_content):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest()

# Check if the file is a duplicate based on its content hash
def check_for_duplicate(file_hash):
    db_connection = connect_db()
    if db_connection is None:
        return False

    cursor = db_connection.cursor()
    query = "SELECT * FROM dataset_metadata WHERE file_hash=%s"
    cursor.execute(query, (file_hash,))
    result = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return bool(result)

@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.get_json()
    file_content = data.get('fileContent').encode('utf-8')
    file_hash = compute_file_hash(file_content)

    if check_for_duplicate(file_hash):
        return jsonify({"message": "Duplicate detected"}), 409
    else:
        return jsonify({"message": "No duplicate found"}), 200

if __name__ == '__main__':
    app.run(port=5000)
