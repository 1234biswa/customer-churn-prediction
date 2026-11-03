# 💻 Installation & Local Setup Guide

This guide provides step-by-step instructions for installing and running **ChurnGuard Enterprise** on your local machine.

---

## 📋 System Prerequisites
* **Python**: Version `3.10` or higher (`python --version`)
* **Git**: Version `2.x` or higher (`git --version`)
* **Operating System**: Windows 10/11, macOS, or Linux

---

## 🛠️ Step-by-Step Installation

### Step 1: Clone the GitHub Repository
Open terminal/command prompt and run:

```bash
git clone https://github.com/your-username/customer-churn-prediction.git
cd customer-churn-prediction
```

---

### Step 2: Create & Activate Virtual Environment

* **On Windows (PowerShell / Command Prompt)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

* **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### Step 3: Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Launch the Streamlit Web Application
```bash
streamlit run app.py
```

The application will launch automatically in your browser at **[http://localhost:8501](http://localhost:8501)**!

---

## 🗄️ Step 5: Database Setup (Optional MySQL Connection)

By default, the application runs out-of-the-box using an **automatic local SQLite database** (`data/customer_churn_db.sqlite`).

If you wish to connect to a live **MySQL database**:

1. Install MySQL Server and create database `customer_churn_db`.
2. Create a `.env` file in the project root:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=customer_churn_db
   ```
3. Run the schema creation script:
   ```bash
   python -c "from src.db import init_db; init_db()"
   ```

---

## 🧪 Step 6: Run Automated Tests & Verification
Run the Pytest suite to verify that all modules are working correctly:

```bash
python -m pytest tests/
```
