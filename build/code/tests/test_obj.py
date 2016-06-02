
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from datetime import datetime

from src.obj import *
from src.op_exceptions import AttributeRequired
from src.op_exceptions import ConstraintError

class TestName(TestCase):
    TESTING = True
    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        # correct name
        self.assertEqual(new_name.value, "John")
        # incorrect name
        self.assertRaises(TypeError, Name, "123dasd")

class TestEmail(TestCase):
    TESTING = True
    def test_email_type(self):
        print "test_email_type"
        new_email = Email("Johnw@gmail.com")
        # correct name
        self.assertEqual(new_email.value, "Johnw@gmail.com")
        # incorrect name
        self.assertRaises(TypeError, Email, "sdfsdfsdfsfsdf")

class TestUser(TestCase):
    TESTING = True
    
 
    def test_user_creation_without_role(self):
        temp = {'name': Name('john'), 'email': Email('john@gmail.com')}
        self.assertRaises(AttributeError,User, temp )

    def test_user_creation_with_role(self):
        temp = {'name': Name('john'), 'email': Email('john@gmail.com') , 'role': Role('admin') }
        inst = User(temp)
        self.assertEqual(inst.get_name(),'john')
        self.assertEqual(inst.get_email(),'john@gmail.com')
        self.assertEqual(inst.get_role(),'admin')

    def test_setemail(self):
        temp = {'name': Name('john'), 'email': Email('john@gmail.com') , 'role': Role('admin') }
        inst = User(temp)
        self.assertEqual(inst.get_email(),'john@gmail.com')
        inst.set_email(Email('john123@gmail.com'));
        self.assertEqual(inst.get_email(),'john123@gmail.com')

    def test_setname(self):
        temp = {'name': Name('john'), 'email': Email('john@gmail.com') , 'role': Role('admin') }
        inst = User(temp)
        self.assertEqual(inst.get_name(),'john')
        inst.set_name(Name('johnsnow'));
        self.assertEqual(inst.get_name(),'johnsnow')

class TestRole(TestCase):
    TESTING = True
    def test_role_creation(self):
        print "test_role"
        new_name = Name("admin")
        # correct name
        self.assertEqual(new_name.value, "admin")
        # incorrect name
        self.assertRaises(TypeError, Role, "adminnormal")

    def test_role_set_name(self):
        temp_role = Role('admin')
        self.assertEqual(temp_role.value,'admin')
        temp_role.set_role('normal')
        self.assertEqual(temp_role.value,'normal')

    def test_role_get_all(self):
        temp_role = Role('admin')
        #self.assertEqual(temp_role.get_all(),('admin','normal'))

class TestSession(TestCase):
    TESTING = True
    

    def test_addsession(self):
        print 'testing session:add session'
        temp = {'name': Name('john'), 'email': Email('john@gmail.com') , 'role': Role('admin') }
        inst = User(temp)
        sess = Session(inst)
        self.assertEqual(inst,sess.get_user())

sys = System()
class TestSystem(TestCase):

    TESTING = True
    
    def setUp(self):
        temp = {'name': Name('john'), 'email': Email('john@gmail.com') , 'role': Role('admin') }
        temp1 = {'name': Name('johnsnow'), 'email': Email('johnsnow@gmail.com') , 'role': Role('normal') }
        inst = User(temp)        
        sessi = Session(inst)
        inst1 = User(temp1)
        sessi1 = Session(inst1)
        global sys
        sys.users.append(inst)
        sys.session_list.append(sessi)
        sys.users.append(inst1)
        sys.session_list.append(sessi1)

    def tearDown(self):
        global sys
        sys.users = []
        sys.session_list = []

    def test_adduser(self):
        print 'testing System: adduser'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        with self.assertRaises(ConstraintError): # trying to add same user
            sys.add_user(normal_logged[0].get_user(),admin_logged)
        with self.assertRaises(ConstraintError): # normal uesr trying to add user
            temp2 = {'name': Name('raj'), 'email': Email('raj@gmail.com') , 'role': Role('admin') }
            inst2 = User(temp2)
            sys.add_user(inst2,normal_logged[0])
        with self.assertRaises(ConstraintError): # proper instances not passed
            temp2 = {'name': Name('raj'), 'email': Email('raj@gmail.com') , 'role': Role('admin') }
            inst2 = User(temp2)
            sys.add_user(admin_logged[0],inst2)

        

    def test_showusers(self):
        print 'testing System: show_users'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        a = sys.show_users(admin_logged[0])
        for i in range(0,len(a)):
            self.assertEqual(str(a[i].get_email()),str(sys.users[i].get_email()))
            self.assertEqual(str(a[i].get_name()),str(sys.users[i].get_name()))
            self.assertEqual(str(a[i].get_role()),str(sys.users[i].get_role()))

    def test_deluser(self):
        print 'testing System: del_users'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        with self.assertRaises(ConstraintError): # normal user trying to delete user
            temp2 = {'name': Name('raj'), 'email': Email('raj@gmail.com') , 'role': Role('normal') }
            inst2 = User(temp2)
            sys.users.append(inst2)
            sys.del_user(inst2,normal_logged[0])
        with self.assertRaises(ConstraintError): # you cannot delete an admin
            temp3 = {'name': Name('raja'), 'email': Email('raja@gmail.com') , 'role': Role('admin') }
            inst3 = User(temp3)
            sys.users.append(inst3)
            sys.del_user(inst3,admin_logged[0])
        with self.assertRaises(ConstraintError): # cannot delete oneself
            sys.del_user(admin_logged[0].get_user(),admin_logged[0])

    def test_getuserbyemail(self):
        print 'testing System: get_user by email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        a = sys.getUserByEmail(Email('john@gmail.com'),admin_logged[0])
        self.assertEqual(a[0].get_name(),'john')
        self.assertEqual(len(a),1)
        self.assertEqual(a[0].get_email(),'john@gmail.com')

    def test_getemail(self):
        print 'testing System: get_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        a = sys.get_email(normal_logged[0].get_user(),admin_logged[0])
        self.assertEqual(a,'johnsnow@gmail.com')

    def test_getname(self):
        print 'testing System: get_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        a = sys.get_name(normal_logged[0].get_user(),admin_logged[0])
        self.assertEqual(a,'johnsnow')

    def test_getemail(self):
        print 'testing System: get_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        a = sys.get_role(admin_logged[0].get_user(),admin_logged[0])
        self.assertEqual(a,'admin')

    def test_setemail(self):
        print 'testing System: set_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        sys.set_email(normal_logged[0].get_user(),Email('johnraj@gmail.com'),admin_logged[0]) # admin changing
        self.assertEqual(normal_logged[0].get_user().get_email(),'johnraj@gmail.com')
        self.assertEqual(sys.getUserByEmail(Email('johnraj@gmail.com'),admin_logged[0])[0],normal_logged[0].get_user())
        sys.set_email(normal_logged[0].get_user(),Email('johnsnow@gmail.com'),admin_logged[0]) # user changing bakc
        self.assertEqual(normal_logged[0].get_user().get_email(),'johnsnow@gmail.com')
        self.assertEqual(sys.getUserByEmail(Email('johnsnow@gmail.com'),admin_logged[0])[0],normal_logged[0].get_user())

    def test_setname(self):
        print 'testing System: set_name'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        sys.set_name(normal_logged[0].get_user(),Name('johnraj'),admin_logged[0]) # admin changing
        self.assertEqual(normal_logged[0].get_user().get_name(),'johnraj')
        sys.set_name(normal_logged[0].get_user(),Name('johnsnow'),normal_logged[0]) # user changing bakc
        self.assertEqual(normal_logged[0].get_user().get_name(),'johnsnow')

    def test_showsessions(self):
        print 'testing System: show session'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()=='admin']
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()=='normal']
        with self.assertRaises(ConstraintError):
            a = sys.showSessions(normal_logged[0])
        b = sys.showSessions(admin_logged[0])
        for i in range(0,len(b)):
            self.assertEqual(str(b[i].get_user().get_email()),str(sys.session_list[i].get_user().get_email()))
            self.assertEqual(str(b[i].get_user().get_name()),str(sys.session_list[i].get_user().get_name()))
            self.assertEqual(str(b[i].get_user().get_role()),str(sys.session_list[i].get_user().get_role()))



if __name__ == '__main__':
    unittest.main()
