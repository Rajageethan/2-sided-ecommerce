import mysql.connector

def create_database():
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password"
    )

    cursor = connection.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
    
    # Use the created database
    cursor.execute("USE ecommerce")

    # Create consumers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consumers (
        consumer_id INT AUTO_INCREMENT PRIMARY KEY,
        consumer_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        town VARCHAR(100) NOT NULL,
        state VARCHAR(100) NOT NULL,
        pincode VARCHAR(10) NOT NULL,
        phone_number VARCHAR(10) NOT NULL
    )
    """)

    # Create farmers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        farmer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        town VARCHAR(100) NOT NULL,
        state VARCHAR(100) NOT NULL,
        pincode VARCHAR(10) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        latitude FLOAT,
        longitude FLOAT,
        address VARCHAR(225)
    )
    """)

    # Create products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        farmer_id INT,
        product_name VARCHAR(100) NOT NULL,
        description TEXT,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        image_url BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
    )
    """)

    # Create orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        consumer_name VARCHAR(100) NOT NULL,
        consumer_email VARCHAR(255),
        quantity INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        farmer_id INT,
        product_name VARCHAR(25),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
    )
    """)

    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_database()
