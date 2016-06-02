
# -*- coding: utf-8 -*-

from collections import OrderedDict

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app, request
from sqlalchemy.orm import relationship
import sqlalchemy.types as types

import os
import re
from urlparse import urlparse
from datetime import datetime
import json
import copy

from op_exceptions import AttributeRequired,ConstraintError
from utils import *


db = SQLAlchemy()


# Abstract class to hold common methods
class Entity(db.Model):

    __abstract__ = True

    # save a db.Model to the database. commit it.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # update the object, and commit to the database
    def update(self, **kwargs):
        for attr, val in kwargs.iteritems():
            setter_method = "set_" + attr
            try:
                self.__getattribute__(setter_method)(val)
            except Exception as e:
                raise e

        self.save()

    #print "Setting new val"
    #print "Calling %s on %s" % (method_to_set, curr_entity)
    #try:
    #    getattr(record, method_to_set)(new_val)
    #except Exception as e:
    #pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Name(object):
    value = None
    def __init__(self, value):
        # value: String
        # if the string contains any non-alphabet and non-space character,
        # raise a type error
        if is_alphabetic_string(value):
            self.value = value
        else:
            raise TypeError('%s is not a Name!' % value)

    def __str__(self):
        return self.value

class Email(object):
    value = None
    def __init__(self, value):
        if not is_email(value):
            raise TypeError('%s is not an email!' % value)
        self.value = value

    def __str__(self):
        return self.value

    def get_email(self):
        return self.value

class User(Entity):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, **kwargs):
        if 'email' not in kwargs:
            raise AttributeRequired("email is mandatory")

        if 'name' not in kwargs:
            raise AttributeRequired("name is mandatory")

        if 'role' not in kwargs:
            raise AttributeRequired("Atleast one role is mandatory")

        self.set_email(kwargs['email'])
        self.set_name(kwargs['name'])
        self.set_role(kwargs['role'])

    def set_role(self, role):
        if not isinstance(role, Role):
            raise TypeError('`role` argument should be of type Role.')
        else:
            self.role = role

    def set_email(self, email):
        if not isinstance(email, Email):
            raise TypeError('`email` argument should be of type Email.')
        else:
            self.email = email.value

    def set_name(self, name):
        if not isinstance(name, Name):
            raise TypeError('`name` argument should be of type Name.')
        else:
            self.name = name.value

    def set_role(self, role):
        if not isinstance(role, Role):
            raise TypeError('`role` argument should be of type Role.')
        else:
            self.role = role

    def get_role(self):
        return self.role

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    @staticmethod
    def get_all():

        db.session.autoflush = False
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    def to_client(self):
        if self.role == Role.get_by_id(1):
            return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': 'admin'
            }
        else :
            return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': 'user'
            }


class Role(Entity):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    users = db.relationship('User', backref='role')

    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise AttributeRequired("name is mandatory")

        self.set_name(kwargs['name'])

    def set_name(self, name):
        if not isinstance(name, Name):
            raise TypeError('`name` argument should be of type Name.')
        else:
            self.name = name.value

    def set_users(self, users):
        type_error = False
        for user in users:
            if not isinstance(user, User):
                type_error = True
                break

        if not type_error:
            self.users = users
        else:
            raise TypeError('`user` argument should be of type User.')

    def get_name(self):
        return self.name

    def get_users(self):
        return self.users

    def get_id(self):
        return self.id

    @staticmethod
    def get_by_id(id):
        return Role.query.get(id)

    @staticmethod
    def get_all():
        return Role.query.all()

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Session():
    user = None

    def __init__(self, user):
        if not isinstance(user,User):
            raise AttributeRequired("user instance not passed")
        else :
            self.user = user;

    def get_user(self):
        return self.user

class System():
    users = []
    session_list = []

    def __init__ (self):
        self.session_list = []


    def add_user(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if session.get_user().get_role().name == 'admin' and session in self.session_list:
                if user.get_email() not in [User.get_all()[i].get_email() for i in range(0,len(User.get_all()))]:
                    user.save()
                else :
                    raise ConstraintError ('User already exists')
                    return False
            else :
                raise ConstraintError ('User must be admin and logged to add a new user')
                return False
        else:
            raise ConstraintError ('instances of user and session must be passed')
            return False


    def add_users_client(self,user,session_email):
        logged_in_list = [s for s in self.session_list if s.get_user().get_email()==session_email]
        if len(logged_in_list)==0:
            raise ConstraintError('session not present')
        else :
            self.add_user(user,logged_in_list[0])


    def show_users(self,session):
        if isinstance(session,Session):
            if session in self.session_list :
                return User.get_all()
            else :
                raise ConstraintError('Session not in session list')
        else:
            raise ConstraintError ('Instance of session not passed')


    def get_users_client(self,mail_id):
        logged_in_list = [s for s in self.session_list if s.get_user().get_email()==mail_id]
        if logged_in_list :
            user_dict_list = []
            for user in self.show_users(logged_in_list[0]):
                user_dict_list.append(user.to_client())
            return user_dict_list
        else :
            raise ConstraintError('user  not logged in')

    def del_user(self,user,session):
        print user.get_role().name
        print user.get_role().name!='admin'
        if isinstance(user,User) and isinstance(session,Session):
            if session.get_user().get_role().name=='admin':  # only an admin can delete
                if user.get_role().name!='admin': # admin cannot be deleted
                    if session.get_user().get_email()!=user.get_email(): # cannot delete oneself
                        if user.get_email() not in [ i.get_user().get_email() for i in self.session_list ]:
                             if user in User.get_all() and session in self.session_list :
                                 user.delete()
                             else :
                                raise ConstraintError('user not in list or session not present')
                        else :
                            raise ConstraintError('logged in user cannot be deleted')
                    else :
                        raise ConstraintError('Cannot delete oneself. Sorry')
                else :
                    raise ConstraintError('admin cannot be deleted')
            else :
                raise ConstraintError('only admin can delete another user')
        else:
            raise ConstraintError ('Instance of user and session not passed')


    def del_users_client(self,id,mail_id):
        logged_in_list = [s for s in self.session_list if s.get_user().get_email()==mail_id]
        print logged_in_list[0].get_user().get_role().name
        if len(logged_in_list)==0:
            raise ConstraintError('session not present')
        else :
            user = User.get_by_id(id)
            if user :
                self.del_user(user,logged_in_list[0])
                return
            raise ConstraintError('no such user exists')


    def getUserByEmail(self,email,session):
        if isinstance(session,Session) and isinstance(email,Email):
            if session in self.session_list:
                return [user for user in User.get_all() if user.get_email()==email.value]
            else :
                raise ConstraintError('session not valid')
        else:
            raise ConstraintError ('Instance of Email and session not passed')

    def get_email(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if user in User.get_all() and session in self.session_list:
                return [u.get_email() for u in User.get_all() if u==user][0]
            else :
                raise ConstraintError('user doesnot exists or invalid session')
        else:
            raise ConstraintError ('Instance of session not passed')


    def get_name(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if user in User.get_all() and session in self.session_list:
                return [u.get_name() for u in User.get_all() if u==user][0]
            else :
                raise ConstraintError('user doesnot exists or invalid session')
        else:
            raise ConstraintError ('Instance of session not passed')

    def get_role(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if user in User.get_all() and session in self.session_list:
                return [u.get_role() for u in User.get_all() if u==user][0]
            else :
                raise ConstraintError('user doesnot exists or invalid session')
        else:
            raise ConstraintError ('Instance of session not passed')

    def set_email(self,user,email,session):
        print 'set_email called here'
        if isinstance(user,User) and isinstance(session,Session) and isinstance(email,Email):
            if session.user.get_role()==Role.get_by_id(1) or session.user==user:
               if user in User.get_all() and session in self.session_list:
                   user.set_email(email)
                   user.update()
               else :
                   raise ConstraintError('user not existing or session expired')
            else :
                raise ConstraintError('Only admin of same user can edit the email')
        else :
            raise ConstraintError ('Proper instances of user,email, session not passed')


    def set_email_client(self,user,new_email,mail_id):
        logged_in_list = [s for s in self.session_list if s.get_user().get_email()==mail_id]
        print len(logged_in_list)
        if len(logged_in_list)==0:
            raise ConstraintError('session not present')
        else :
            self.set_email(user,Email(new_mail),logged_in_list[0])


    def set_name(self,user,name,session):
        if isinstance(user,User) and isinstance(session,Session) and isinstance(name,Name):
            if session.user.get_role().name=='admin' or session.user==user:
               if user in User.get_all() and session in self.session_list:
                   user.set_name(name)
                   user.update()
               else :
                   raise ConstraintError('user not existing or session expired')
            else :
                raise ConstraintError('Only admin of same user can edit the name')
        else :
            raise ConstraintError ('Proper instances of user,email, session not passed')


    def set_name_client(self,user,new_name,mail_id):
        logged_in_list = [s for s in self.session_list if s.get_user().get_email()==mail_id]
        if len(logged_in_list)==0:
            raise ConstraintError('session not present')
        else :
            self.set_name(user,Name(new_name),logged_in_list[0])




    def update_user(self,user,email,name,session):
        print 'update_user called here'
        if isinstance(user,User) and isinstance(session,Session) and isinstance(email,Email) and isinstance(name,Name):
            if session.get_user().get_role().name=='admin' or session.user.get_email()==user.get_email():
                if email.value not in [i.get_email() for i in User.get_all()]:
                   if user in User.get_all() and session in self.session_list :
                       print 'almost update passed all barriers'
                       user.set_email(email)
                       user.set_name(name)
                       user.update()
                   else :
                       raise ConstraintError('user not existing or session expired')
                else :
                    raise ConstraintError('Email already exists, so cannot add')
            else :
                raise ConstraintError('Only admin of same user can edit the email')
        else :
            raise ConstraintError ('Proper instances of user,email, session not passed')


    def update_user_client(self,user,new_name,new_email,mail_id):
        print 'update_user_client'
        logged_in_list = [s for s in self.session_list if s.get_user().get_email()==mail_id]
        print len(logged_in_list)
        if len(logged_in_list)==0:
            raise ConstraintError('session not present')
        else :
            self.update_user(user,Email(new_email),Name(new_name),logged_in_list[0])

    def showSessions(self,session):
        if  isinstance(session,Session):
            if session in self.session_list:
               if session.get_user().get_role() == Role.get_by_id(1):
                   return self.session_list[:]
               else :
                   raise ConstraintError('only admin can get session list')
            else :
                raise ConstraintError('session expired')
        else :
            raise ConstraintError ('instance of session class has to be passed')

    def login_client(self,mail_id):

        if mail_id in [i.get_user().get_email() for i in self.session_list]:
            return True
        else :
            return False

sys = System()





def login_user(user,sys):

    if isinstance(user,User) and isinstance(sys,System):
        sessi = Session(user)
        sys.session_list.append(sessi)
    else :
        raise ConstraintError('user and system instances required')

def logout_client(mail_id,sys):

    for i in sys.session_list:
        if i.get_user().get_email()==mail_id:
            sys.session_list.remove(i)
