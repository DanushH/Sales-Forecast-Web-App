CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    store VARCHAR(100) NOT NULL,
    product VARCHAR(100) NOT NULL,
    prediction FLOAT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
