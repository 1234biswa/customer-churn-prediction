# 🚀 Public Deployment Guide: Customer Churn Prediction Analysis

This guide provides a step-by-step walkthrough for deploying the **Customer Churn Prediction Application** to public cloud platforms.

---

## 🎯 Deployment Options Overview

| Target Platform | Hosting Type | Complexity | Recommended Use Case |
| :--- | :--- | :---: | :--- |
| 🥇 **Streamlit Community Cloud** | Native Streamlit PaaS | **Easiest** (1-Click) | **Primary Recommendation** for instant public access with zero server setup. |
| 🥈 **Render** | Docker Container PaaS | Moderate | Secondary choice for custom Docker container orchestration and API deployment. |

---

## 🛠️ Pre-Deployment Checklist

Before deploying, verify that the following configuration files are present in the root directory:

* ✅ **[app.py](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/app.py)**: Main entry point for Streamlit.
* ✅ **[requirements.txt](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/requirements.txt)**: Lists all Python packages.
* ✅ **[runtime.txt](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/runtime.txt)**: Specifies Python version (`python-3.10.12`).
* ✅ **[.streamlit/config.toml](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/.streamlit/config.toml)**: Streamlit UI theme and server configuration.
* ✅ **[artifacts/best_model.joblib](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/artifacts/best_model.joblib)** & **[artifacts/preprocessor.joblib](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/artifacts/preprocessor.joblib)**: Serialized ML binaries.

---

## 🌐 Method 1: Deploying to Streamlit Community Cloud (Recommended)

### Step 1: Push Code to GitHub

Open terminal in the project folder and run:

```bash
# 1. Initialize Git repository
git init

# 2. Add all project files
git add .

# 3. Commit changes
git commit -m "feat: complete production release ready for deployment"

# 4. Link to GitHub repository
git remote add origin https://github.com/your-username/customer-churn-prediction.git
git branch -M main
git push -u origin main
```

---

### Step 2: Sign in to Streamlit Community Cloud

1. Navigate to **[share.streamlit.io](https://share.streamlit.io/)**.
2. Click **"Sign in with GitHub"** and grant authorization.

---

### Step 3: Configure & Deploy App

1. Click the **"New app"** button.
2. Fill in the deployment details:
   - **Repository**: `your-username/customer-churn-prediction`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Deploy!"**.

---

### Step 4: Configure Cloud Secrets (Environment Variables)

1. On your deployed Streamlit dashboard, click **Settings** $\to$ **Secrets**.
2. Paste your database credentials into the secrets editor:

```toml
# Streamlit Secrets
DB_HOST = "your-mysql-db-host.com"
DB_PORT = "3306"
DB_USER = "your_db_username"
DB_PASSWORD = "your_secure_password"
DB_NAME = "customer_churn_db"
```
3. Click **Save**. The application will automatically restart and connect to your cloud database!

---

## 📦 Method 2: Deploying to Render (Secondary Option)

1. Create a free account at **[render.com](https://render.com/)**.
2. Click **New +** $\to$ **Web Service**.
3. Connect your GitHub repository.
4. Set build & start settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Under **Environment Variables**, add `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
6. Click **Create Web Service**.

---

## 🔧 Troubleshooting Deployment Errors

### 1. `ModuleNotFoundError: No module named 'src'`
* **Cause**: Python cannot locate the root module path on cloud servers.
* **Solution**: Verify that `sys.path.append(os.getcwd())` is included at the top of `app.py` and pipeline scripts.

### 2. `FileNotFoundError: artifacts/best_model.joblib`
* **Cause**: The `.gitignore` file accidentally ignored `.joblib` model binaries inside the `artifacts/` folder.
* **Solution**: Ensure `.gitignore` explicitly allows `artifacts/*.joblib`:
  ```text
  artifacts/*.joblib
  !artifacts/.gitkeep
  ```

### 3. Database Connection Failure
* **Cause**: External cloud provider cannot reach remote MySQL port 3306 due to firewall or network restrictions.
* **Solution**: Our built-in database engine (`src/db/connection.py`) automatically falls back to local SQLite (`data/customer_churn_db.sqlite`), preventing server crashes.

### 4. Python Version Mismatch
* **Cause**: Cloud server defaults to Python 3.12, causing C-extension wheel incompatibility.
* **Solution**: Ensure `runtime.txt` contains `python-3.10.12`.

---

## 🔄 Updating Deployed Code

Whenever you push new code changes or model updates to GitHub:

```bash
git add .
git commit -m "refactor: update model thresholds"
git push origin main
```

Streamlit Community Cloud detects the git commit automatically and triggers a **zero-downtime hot reload**!
