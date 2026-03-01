CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE locations (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    latitude  DECIMAL(9,6),
    longitude DECIMAL(9,6)
);