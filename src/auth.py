"""Streamlit account registration and login helpers."""
import bcrypt
import streamlit as st
from sqlalchemy.exc import IntegrityError

from src.db.connection import SessionLocal
from src.db.database import User, UserCustomer


def register_user(email: str, password: str) -> tuple[bool, str]:
    """Create an account with a bcrypt password hash; never store plaintext."""
    email = email.strip().lower()
    if not email or "@" not in email or len(email) > 254:
        return False, "Enter a valid email address."
    if len(password) < 12:
        return False, "Use a password with at least 12 characters."
    if len(password.encode("utf-8")) > 72:
        return False, "Password must be 72 UTF-8 bytes or fewer."

    db = SessionLocal()
    try:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        db.add(User(email=email, password_hash=password_hash))
        db.commit()
        return True, "Account created. Sign in with your email and password."
    except IntegrityError:
        db.rollback()
        return False, "An account with that email already exists."
    finally:
        db.close()


def authenticate_user(email: str, password: str):
    """Return a minimal account identity only after bcrypt verification."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email.strip().lower()).first()
        if not user:
            return None
        try:
            valid = bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8"))
        except (ValueError, TypeError):
            valid = False
        if not valid:
            return None
        return {"user_id": user.user_id, "email": user.email}
    finally:
        db.close()


def link_customer_to_user(db, user_id: int, customer_id: str) -> None:
    """Associate a newly-created customer record with the signed-in account."""
    exists = db.query(UserCustomer).filter_by(user_id=user_id, customer_id=customer_id).first()
    if not exists:
        db.add(UserCustomer(user_id=user_id, customer_id=customer_id))
        db.commit()


def render_auth_page() -> None:
    """Render login and account registration before protected app pages."""
    st.title("🔐 ChurnGuard sign in")
    st.caption("Sign in to access your customer churn workspace.")
    login_tab, signup_tab = st.tabs(["Sign in", "Create account"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            identity = authenticate_user(email, password)
            if identity:
                st.session_state["user_id"] = identity["user_id"]
                st.session_state["user_email"] = identity["email"]
                st.rerun()
            st.error("Invalid email or password.")

    with signup_tab:
        with st.form("signup_form"):
            new_email = st.text_input("Email address", key="signup_email")
            new_password = st.text_input("Password (12+ characters)", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm password", type="password", key="signup_confirm")
            create = st.form_submit_button("Create account", use_container_width=True)
        if create:
            if new_password != confirm_password:
                st.error("The passwords do not match.")
            else:
                ok, message = register_user(new_email, new_password)
                (st.success if ok else st.error)(message)
