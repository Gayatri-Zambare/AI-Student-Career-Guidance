import os

# Production Gunicorn configuration for Render, Railway, Heroku, and Linux deployments
port = os.environ.get("PORT", "5000")
bind = f"0.0.0.0:{port}"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = 2
timeout = 120
accesslog = "-"
errorlog = "-"
keepalive = 5
