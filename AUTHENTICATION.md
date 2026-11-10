# Authentication setup

ChurnGuard now includes application-level account registration and sign-in for its Streamlit interface.

## How it works

- Users register with an email address and a password of at least 12 characters.
- Passwords are hashed with bcrypt before storage in the `users` table. Plaintext passwords are never stored.
- Successful login places the account ID and email in Streamlit's server-side session state for the active browser session.
- New customer records are linked to the signed-in account in `user_customers`; dashboard and history queries filter through that ownership mapping.
- Logging out clears the session identity.

## Install and run

Install the updated dependencies, then start the app as usual:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The `users` and `user_customers` tables are created by the existing database initialization. Existing customer and prediction rows are not automatically assigned to a user and therefore do not appear in a new account's history. Back up your database before deploying schema changes.

## Important deployment notes

- Use HTTPS in production.
- Set a strong, unique database password and use a least-privilege database account.
- Keep database credentials in deployment secrets; never commit `.env` files.
- Streamlit session state is session-scoped, not a persistent “remember me” token. Closing/restarting the browser session may require signing in again.
- This implementation does not create JWTs, refresh tokens, OAuth, password-reset emails, email verification, or an API authentication layer. Those require a separately deployed API/session architecture.
- Configure rate limiting or an identity provider before exposing public self-registration to the internet.
