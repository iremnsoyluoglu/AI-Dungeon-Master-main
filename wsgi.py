#!/usr/bin/env python3
"""
WSGI Entry Point for Vercel Deployment
======================================
This file serves as the entry point for Vercel to run the Flask application
"""

from simple_app import app

# Export the Flask app for Vercel
if __name__ == '__main__':
    app.run()
