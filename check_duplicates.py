import mysql.connector
import hashlib
from datetime import datetime
import os
import json

def connect_db():
    """Connect to the MySQL database."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="aditya99",  # Replace with your MySQL username
            password="Aditya#99",  # Replace with your MySQL password
            database="ddas"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def compute_file_hash(file_path):
    """Compute the SHA-256 hash of the file content."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest().lower()  # Convert hash to lowercase
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error computing file hash: {e}")
        return None

def check_for_duplicate(file_hash):
    """Check if the file is a duplicate based on its content hash."""
    db_connection = connect_db()
    if db_connection is None:
        return False

    cursor = db_connection.cursor()

    query = """
    SELECT * FROM dataset_metadata
    WHERE LOWER(file_hash)=%s
    """
    
    cursor.execute(query, (file_hash.lower(),))
    result = cursor.fetchall()

    cursor.close()
    db_connection.close()

    if result:
        return True  # Duplicate found
    else:
        return False  # No duplicate found

def save_file_metadata(file_name, file_size, file_hash, user_id, download_location):
    """Save the file metadata into the database."""
    db_connection = connect_db()
    if db_connection is None:
        return

    cursor = db_connection.cursor()

    query = """
    INSERT INTO dataset_metadata (file_name, file_size, download_timestamp, user_id, file_hash, download_location)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    download_timestamp = datetime.now()
    
    cursor.execute(query, (file_name, file_size, download_timestamp, user_id, file_hash, download_location))
    db_connection.commit()
    
    print("File metadata saved successfully.")
    
    cursor.close()
    db_connection.close()

def save_message_to_json(message):
    """Save the status message to a JSON file."""
    data = {
        "lastMessage": message
    }
    with open('status.json', 'w') as json_file:
        json.dump(data, json_file)
    print(f"Status message saved to status.json: {message}")

def upload_file(file_path, user_id):
    """Attempt to upload a file, checking for duplicates first."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_hash = compute_file_hash(file_path)

    if not file_hash:
        message = "File upload failed: Unable to compute file hash."
        print(message)
        save_message_to_json(message)
        return

    if check_for_duplicate(file_hash):
        message = "File upload failed: Duplicate content detected. File not uploaded."
        print(message)
        save_message_to_json(message)
    else:
        message = "No duplicate found. Uploading file..."
        print(message)
        download_location = os.path.dirname(file_path)
        save_file_metadata(file_name, file_size, file_hash, user_id, download_location)
        message = "File uploaded successfully."
        print(message)
        save_message_to_json(message)

# Example usage:
user_id = "12345"  # Replace with the actual user ID or fetch dynamically
file_path = "C:/Users/Singh/Desktop/DDAS/sample.txt"  # Replace with the actual file path
upload_file(file_path, user_id)
