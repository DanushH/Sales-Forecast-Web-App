CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    user_email VARCHAR(100) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL
);

CREATE TABLE prediction (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_date DATE NOT NULL,
    prediction_country VARCHAR(100) NOT NULL,
    prediction_store VARCHAR(100) NOT NULL,
    prediction_product VARCHAR(100) NOT NULL,
    prediction_prediction FLOAT NOT NULL,
    prediction_user_id INT,
    FOREIGN KEY (prediction_user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

ALTER TABLE prediction
	ADD CONSTRAINT unique_prediction 
		UNIQUE (
            prediction_user_id, 
            prediction_date, 
            prediction_country, 
            prediction_store, 
            prediction_product
        );


CREATE TABLE activity (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_user_id INT NOT NULL,
    activity_action VARCHAR(255) NOT NULL,
    activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

DELIMITER $$

CREATE TRIGGER log_user_predictions
AFTER INSERT ON prediction
FOR EACH ROW
BEGIN
    INSERT INTO activity (activity_user_id, activity_action)
    VALUES (
        NEW.prediction_user_id, 
        CONCAT('Made a prediction with prediction_id: ', NEW.prediction_id)
    );
END$$

DELIMITER ;
