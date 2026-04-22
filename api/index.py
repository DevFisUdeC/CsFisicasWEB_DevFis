"""
Entrypoint para Vercel Serverless (Python runtime).
"""

from app import create_app


app = create_app("production")
