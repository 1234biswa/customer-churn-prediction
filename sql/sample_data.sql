-- Seed Sample Data for Customer Churn Prediction Database
USE customer_churn_db;

-- Seed Sample Customers
INSERT INTO customers (customer_id, gender, senior_citizen, partner, dependents, tenure, phone_service, internet_service, contract, payment_method, monthly_charges, total_charges)
VALUES 
('7590-VHVEG', 'Female', 0, 'Yes', 'No', 1, 'No', 'DSL', 'Month-to-month', 'Electronic check', 29.85, 29.85),
('5575-GNVDE', 'Male', 0, 'No', 'No', 34, 'Yes', 'DSL', 'One year', 'Mailed check', 56.95, 1889.50),
('3668-QPYBK', 'Male', 0, 'No', 'No', 2, 'Yes', 'DSL', 'Month-to-month', 'Mailed check', 53.85, 108.15);

-- Seed Sample Model Info
INSERT INTO model_info (model_name, algorithm, accuracy, precision_score, recall_score, f1_score, roc_auc, version)
VALUES 
('Gradient Boosting Champion', 'GradientBoostingClassifier', 0.8048, 0.6656, 0.5321, 0.5914, 0.8438, '1.0.0');

-- Seed Sample Application Logs
INSERT INTO application_logs (event_type, description, status)
VALUES 
('Database Connected', 'Successfully initialized relational database engine', 'SUCCESS'),
('Application Started', 'Streamlit application launched successfully', 'SUCCESS');
