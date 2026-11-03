-- Customer Churn Prediction Analysis Database Schema
-- Database: customer_churn_db

CREATE DATABASE IF NOT EXISTS customer_churn_db;
USE customer_churn_db;

-- 1. Table: customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    senior_citizen INT NOT NULL DEFAULT 0,
    partner VARCHAR(5) NOT NULL,
    dependents VARCHAR(5) NOT NULL,
    tenure INT NOT NULL DEFAULT 0,
    phone_service VARCHAR(5) NOT NULL,
    internet_service VARCHAR(20) NOT NULL,
    contract VARCHAR(20) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    monthly_charges DECIMAL(10, 2) NOT NULL,
    total_charges DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table: predictions
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    prediction VARCHAR(20) NOT NULL,
    probability DECIMAL(5, 4) NOT NULL,
    risk_level VARCHAR(30) NOT NULL,
    confidence_score DECIMAL(5, 4) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    prediction_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- 3. Table: model_info
CREATE TABLE IF NOT EXISTS model_info (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    algorithm VARCHAR(100) NOT NULL,
    accuracy DECIMAL(5, 4) NOT NULL,
    precision_score DECIMAL(5, 4) NOT NULL,
    recall_score DECIMAL(5, 4) NOT NULL,
    f1_score DECIMAL(5, 4) NOT NULL,
    roc_auc DECIMAL(5, 4) NOT NULL,
    training_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(20) NOT NULL
);

-- 4. Table: application_logs
CREATE TABLE IF NOT EXISTS application_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
