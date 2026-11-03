# 🤝 Contributing to ChurnGuard Enterprise

Thank you for your interest in contributing to **Customer Churn Prediction Analysis (ChurnGuard Enterprise)**! We welcome bug fixes, feature additions, and documentation enhancements.

---

## 📜 Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 🛠️ How to Contribute

### 1. Fork & Clone
Fork the repository on GitHub and clone your fork locally:

```bash
git clone https://github.com/your-username/customer-churn-prediction.git
cd customer-churn-prediction
```

### 2. Create a Feature Branch
Use descriptive branch names (`feat/`, `fix/`, `docs/`):

```bash
git checkout -b feat/add-fastapi-endpoint
```

### 3. Make Changes & Run Tests
Make your code edits and verify that all automated unit tests pass:

```bash
python -m pytest tests/
```

### 4. Commit Changes
Follow clear git commit conventions:

```bash
git commit -m "feat: add FastAPI prediction endpoint handler"
```

### 5. Push & Open Pull Request
Push your branch to GitHub and submit a Pull Request (PR) against the `main` branch.

---

## 🧪 Code Style & Guidelines
* Follow **PEP-8** formatting standards.
* Add docstrings to all new functions and classes.
* Ensure log messages use the centralized logger (`src/utils/logger.py`).
