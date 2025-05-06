-- Create database
CREATE DATABASE IF NOT EXISTS file_register_db;
USE file_register_db;

-- Create table for file records
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    sender VARCHAR(255) NOT NULL,
    receiver VARCHAR(255) NOT NULL,
    despatched_to VARCHAR(255),
    date_added DATETIME NOT NULL,
    remarks TEXT,
    delete_item TEXT
);

-- Create a user for the application (change password as needed)
CREATE USER IF NOT EXISTS 'file_app_user'@'localhost' IDENTIFIED BY 'Hell0W0Rld';
GRANT ALL PRIVILEGES ON file_register_db.* TO 'file_app_user'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS signup (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    passwd VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL
);