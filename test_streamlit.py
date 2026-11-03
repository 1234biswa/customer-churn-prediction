import os
import sys
import py_compile
import pytest
sys.path.append(os.getcwd())

def test_streamlit_app_compilation():
    """Verifies that app.py and Streamlit components compile without syntax errors."""
    app_path = os.path.join("app.py")
    styles_path = os.path.join("src", "utils", "styles.py")

    assert os.path.exists(app_path), "app.py does not exist!"
    assert os.path.exists(styles_path), "styles.py does not exist!"

    py_compile.compile(app_path, doraise=True)
    py_compile.compile(styles_path, doraise=True)
