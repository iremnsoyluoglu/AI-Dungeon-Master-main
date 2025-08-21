from flask import Flask, request, jsonify, render_template
import sys
import os

# Add parent directory to path to import test_vercel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_vercel import app

# Add CORS headers to bypass authentication issues
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Override any authentication requirements
@app.before_request
def before_request():
    # Bypass any authentication checks
    pass

# Export the app for Vercel
handler = app
