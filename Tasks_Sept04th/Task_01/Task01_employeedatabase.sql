CREATE DATABASE company_db;
USE company_db;

CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    department VARCHAR(50),
    salary DECIMAL(10,2)
);

INSERT INTO employees (first_name, last_name, age, department, salary)
VALUES
('Rahul', 'Sharma', 30, 'IT', 55000.00),
('Anita', 'Kumar', 28, 'Finance', 48000.00),
('Vikram', 'Singh', 35, 'HR', 60000.00),
('Priya', 'Mehta', 26, 'IT', 52000.00),
('Rohan', 'Patel', 32, 'Sales', 45000.00);

SELECT * FROM employees;

SELECT first_name, department, salary FROM employees;

SELECT * FROM employees WHERE department = 'IT';

UPDATE employees
SET department = 'Accounts'
WHERE department = 'Finance'
LIMIT 1;

DELETE FROM employees
WHERE department = 'HR'
LIMIT 1;

SELECT * FROM employees;
