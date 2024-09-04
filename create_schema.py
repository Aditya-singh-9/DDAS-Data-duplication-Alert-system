import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="aditya99",
        password="Aditya#99",
        database="ddas"
    )

def create_table():
    db_connection = connect_db()
    cursor = db_connection.cursor()
    
    create_table_query = """
    CREATE TABLE dataset_metadata (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        file_size BIGINT,
        download_timestamp DATETIME,
        user_id VARCHAR(255),
        file_hash CHAR(64),
        download_location VARCHAR(255)
    );
    """
    
    cursor.execute(create_table_query)
    db_connection.commit()
    
    print("Table created successfully")
    
    cursor.close()
    db_connection.close()

# Run the function to create the table
create_table()
