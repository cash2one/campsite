DEBUG = True

# Set app directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# app.config["APPLICATION_ROOT"] = "/ninjawarriors"

print __file__

THREADS_PER_PAGE = 2

# Protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

CSRF_SESSION_KEY = "secret"

SECRET_KEY = "secret"