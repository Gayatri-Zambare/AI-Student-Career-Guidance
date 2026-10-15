import os
import sys

# Add project root directory to sys.path so app and local modules can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app

# Vercel serverless functions look for `app` WSGI application callable
if __name__ == "__main__":
    app.run(debug=True)
