#
# Application pages/views
#
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
                                    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
                                    verify_jwt_in_request)
from flask import Flask, render_template, request, redirect, url_for
from app import app
import sys

@app.route('/', methods=['GET'])
def front(name=None):
    return render_template('index.html')

@app.route('/logSign', methods=['GET'])
def login():
    return render_template('logSign.html')

@app.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard():
    user = get_raw_jwt()['identity']
    return render_template('dashboard.html', user=user)