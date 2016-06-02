
# -*- coding: utf-8 -*-
from op_exceptions import AttributeRequired
from op_exceptions import ConstraintError
from utils import *
import copy

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
        if is_email(value) :
           self.value = value
        else :
           raise TypeError('%s is not a Email!' % value)

    def __str__(self):
        return self.value
        

    def get_email(self):
        return self.value

class User():
    email = None
    name = None
    role = None

    def __init__(self, kwargs):
        if 'name' not in kwargs or 'email' not in kwargs or 'role' not in kwargs:
            raise AttributeError("argument should be a dict with keys name, email and role")

        elif not isinstance(kwargs['name'],Name)  :
            raise AttributeError("name key must have an instance of Name class")

        elif not isinstance(kwargs['email'],Email)  :
            raise AttributeError("email key must have an instance of Email class")

        elif not isinstance(kwargs['role'],Role)  :
            raise AttributeError("role key must have an instance of Role class")

        else :
            self.name = kwargs['name']
            self.email = kwargs['email']
            self.role = kwargs['role']
           

    def set_email(self, email):
        if isinstance(email,Email):
            self.email = email
        else :
            raise TypeError('argument must be an istance of email class')

    def set_name(self, name):
        if isinstance(name,Name):
            self.name = name;
        else :
            raise TypeError('argument must be an istance of Name class')
        

    def set_role(self, role):
        if isinstance(role,Role):
            self.role = role;
        else :
            raise TypeError('attribute must be an istance of Role class')

    def get_role(self):
        return self.role.value

    def get_email(self):
        return self.email.value

    def get_name(self):
        return self.name.value

    def to_client(self):
        pass
#        return {
#            'name': self.name,
#            'email': self.email,
#            'role': self.role.to_client()
#        }

class Role():
    value = None

    def __init__(self, string):
        if is_role(string)==False:
            raise TypeError("Role can be admin or normal")
        else :
            self.value = string

    def set_role(self, name):
        if is_role(name)==False :
            raise TypeError("role can be admin or normal")
        else :
            self.value = name

    def get_role(self):
        return self.value

    @staticmethod
    def get_all():
#        return ('admin','normal')
        pass

    def to_client(self):
        print "fill"

class Session():
    user = None

    def __init__(self, user):
        if not isinstance(user,User):
            raise TypeError('only instnaces of user class can get session')
        self.user = user

    def get_user(self):
            return self.user

class System():
    users = []
    session_list = []

  
    def add_user(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if session.get_user().get_role()=='admin':
                if user.get_email() not in [self.users[i].get_email() for i in range(0,len(self.users))]:
                    self.users.append(user)
                    return True
                else :
                    raise ConstraintError ('User already exists')
                    return False
            else :
                raise ConstraintError ('User must be admin to add a new user')
                return False
        else:
            raise ConstraintError ('instances of user and session must be passed')            
            return False

  
    def show_users(self,session):
        if isinstance(session,Session):
            if session in self.session_list :
                return copy.deepcopy(self.users)
            else :
                raise ConstraintError('Session not in session list')
        else:
            raise ConstraintError ('Instance of session not passed')            

    def del_user(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if session.get_user().get_role()=='admin' and user.get_role()!='admin' and session.get_user()!=user:
                 if user in self.users and session in self.session_list :
                    self.users.remove(user)
                 else :
                    raise ConstraintError('user not in list or session not present')
            else :
                raise ConstraintError('only admin can delete and admin cannot be removed')
        else:
            raise ConstraintError ('Instance of user and session not passed')            

 
    def getUserByEmail(self,email,session):
        if isinstance(session,Session) and isinstance(email,Email):
            if session in self.session_list:
                return [user for user in self.users if user.get_email()==email.get_email()]
            else :
                raise ConstraintError('session not valid')
        else:
            raise ConstraintError ('Instance of Email and session not passed')     

    def get_email(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if user in self.users and session in self.session_list:
                return [u.get_email() for u in self.users if u==user][0]
            else :
                raise ConstraintError('user doesnot exists or invalid session')
        else:
            raise ConstraintError ('Instance of session not passed')            

 
    def get_name(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if user in self.users and session in self.session_list:
                return [u.get_name() for u in self.users if u==user][0]
            else :
                raise ConstraintError('user doesnot exists or invalid session')
        else:
            raise ConstraintError ('Instance of session not passed')            

    def get_role(self,user,session):
        if isinstance(user,User) and isinstance(session,Session):
            if user in self.users and session in self.session_list:
                return [u.get_role() for u in self.users if u==user][0]
            else :
                raise ConstraintError('user doesnot exists or invalid session')
        else:
            raise ConstraintError ('Instance of session not passed')            

    def set_email(self,user,email,session):
        if isinstance(user,User) and isinstance(session,Session) and isinstance(email,Email):
            if session.user.get_role()=='admin' or session.user==user:
               if user in self.users and session in self.session_list:
                   for i in range(0,len(self.users)):
                       if self.users[i] == user:
                           user.email = email
                           self.users[i] = user
               else :
                   raise ConstraintError('user not existing or session expired')
            else :
                raise ConstraintError('Only admin of same user can edit the email')
        else :
            raise ConstraintError ('Proper instances of user,email, session not passed')

 
    def set_name(self,user,name,session):
        if isinstance(user,User) and isinstance(session,Session) and isinstance(name,Name):
            if session.user.get_role()=='admin' or session.user==user:
               if user in self.users and session in self.session_list:
                   for i in range(0,len(self.users)):
                       if self.users[i] == user:
                           user.name = name
                           self.users[i] = user
               else :
                   raise ConstraintError('user not existing or session expired')
            else :
                raise ConstraintError('Only admin of same user can edit the email')
        else :
            raise ConstraintError ('Proper instances of user,email, session not passed')

    def showSessions(self,session):
        if  isinstance(session,Session):
            if session in self.session_list:
               if session.get_user().get_role() == 'admin':
                   return self.session_list[:]
               else :
                   raise ConstraintError('only admin can get session list')
            else :
                raise ConstraintError('session expired')
        else :
            raise ConstraintError ('instance of session class has to be passed')



def login(user,sys):
    
    if isinstance(user,User) and isinstance(sys,System):
        sessi = Session(user)
        sys.session_list.append(sessi)
    else :
        raise ConstraintError('user and system instances required')

def del_session(session,sys):

    if isinstance(session,Session) and isinstance(sys,System):
        if session in self.session_list:
            sys.session_list.remove(session)
        else :
            raise ConstraintError('session expired')
    else :
        raise ConstraintError('Session and system instances required')
