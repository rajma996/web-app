
# -*- coding: utf-8 -*-

import os
import csv
import requests
from datetime import datetime
import inspect
from flask import session, render_template, Blueprint, request, jsonify, abort,\
    current_app, redirect, url_for
from config import *
from flask import current_app

from flask import Flask, redirect, url_for
from werkzeug import secure_filename

from db import *
from utils import parse_request, jsonify_list
api = Blueprint('APIs', __name__)

from db import sys

@api.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        if ('email' in session):
            return render_template("user-list.html")
        else:
            return render_template("login.html")


#+BEGIN_SRC python :tangle ../../src/api.py :eval no
@api.route("/auth/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = str(request.form['email'])
        user_list = User.get_all()
        for i in range(0,len(user_list)):
            if str(email) == str(user_list[i].get_email()):
                current_app.logger.info("Successfully Logged in")
                session['email'] = email
                session['user_id'] = user_list[i].id
                login_user(user_list[i],sys)
                if user_list[i].get_role() == Role.get_by_id(1) :
                    session['role_name'] = str('admin')
                else :
                    session['role_name'] = str('user')

                return redirect("/")
        return render_template("login.html", message="Invalid email id")

@api.route('/auth/logout', methods=['GET'])
def logout_handler():
    logout_email = str(session['email'])
    session.pop('email', None)
    session.pop('role_name', None)
    logout_client(logout_email,sys)
    return redirect("/")

@api.route('/users', methods=['GET'])
def get_users():

    email =  request.headers.get('session')
    if email in [i.get_user().get_email() for i in sys.session_list]:
        try:
            result = sys.get_users_client(email)
        except:
            abort(503,'not logged in')
        else :
            return jsonify_list(result)

@api.route('/roles', methods=['GET'])
def get_roles():
    if 'session' not in request.json:
        print "throw error from get_roles"
    else:
        print "get_roles -- Check according to your specification"

    return jsonify_list([i.to_client() for i in Role.get_all()])

@api.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    record = User.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("user", id))
    return jsonify(record.to_client())

@api.route('/roles/<int:id>', methods=['GET'])
def get_role_by_id(id):
    record = Role.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("role", id))

    return jsonify(record.to_client())

# not implemented for session, implement with session
@api.route('/users/', methods=['POST'])
def create_user():

    ### Check if there is a session and act according to the specification

    if not request.json or not 'name' in request.json or not 'email' in request.json or not 'role' in request.json:
        abort(400)
    else:
        name = request.json['name']
        email = request.json['email']
        session_email = request.json['session']
        role = request.json['role']

        try:
            if role == 'admin':
                role_id = 1
            else :
                role_id = 2
            user = User(name=Name(name),
                        email=Email(email),
                        role=Role.get_by_id(role_id))

            sys.add_users_client(user,session_email)
            return jsonify(user.to_client())
        except ConstraintError as erro:
            print erro.str
            return jsonify ( {'error' : erro.str } )
        except Exception, e:
            return jsonify({'error' : 'some error occured make sure email id is unique.'})
            current_app.logger.error("Error occured while inserting"
                                     "user record: %s" % str(e))
            abort(500, str(e))

@api.route('/users/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_user(id):

    ### Check if there is a session and act according to the specification
    if not request.headers.get('session'):
        abort(500,'session required')
    else:
        print "Check according to your specification"

    record = User.get_by_id(id)

    if not record:
        abort(404, 'No %s with id %s' % (user, id))

    if request.method == 'DELETE':

        logged_in_email = request.headers.get('session')

        try:
            sys.del_users_client(id,logged_in_email)
            return jsonify(id=id, status="success")
        except ConstraintError as erro:
            return jsonify({'error' : erro.str})
        except Exception, e:
            current_app.logger.error("Error occured while deleting"
                                     "user record %d: %s" % (id, str(e)))
            abort(500, str(e))

    if request.method == 'PUT':

        new_data = {}
        try:
            if 'name' in request.json:
                new_data['name'] = Name(request.json['name'])
            if 'email' in request.json:
                new_data['email'] = Email(request.json['email'])

            sys.update_user_client(record,request.json['name'],request.json['email'],request.json['session'])

            return jsonify(User.get_by_id(id).to_client())

        except ConstraintError as erro:
            return jsonify({'error' : erro.str})
        except Exception, e:
            current_app.logger.error("Error occured while updating"
                                     " user record %d: %s" % (id, str(e)))
            abort(500, str(e))
