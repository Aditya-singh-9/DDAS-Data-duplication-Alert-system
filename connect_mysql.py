import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="aditya99",
        password="Aditya#99",
        database="ddas"
    )

def check_for_duplicates(file_name, file_hash):
    db_connection = connect_db()
    cursor = db_connection.cursor()
    
    query = ("SELECT * FROM dataset_metadata WHERE file_name = %s AND file_hash = %s")
    cursor.execute(query, (file_name, file_hash))
    
    result = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    if result:
        print("Duplicate found:", result)
    else:
        print("No duplicate found")

# Example usage
check_for_duplicates('example_file.csv', 'abcdef123456...')
