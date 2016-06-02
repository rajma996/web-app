
# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
from datetime import datetime
# import json

from src.db import *
from src.app import create_app
from src.op_exceptions import AttributeRequired
from src.op_exceptions import ConstraintError

config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

class TestName(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        # correct name
        self.assertEqual(new_name.value, "John")
        # incorrect name
        self.assertRaises(TypeError, Name, "123dasd")

class TestEmail(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_email_type(self):
        print "test_email_type"
        new_email = Email("smith@gmail.com")
        # correct name
        self.assertEqual(new_email.value, "smith@gmail.com")
        # incorrect name
        self.assertRaises(TypeError, Email, "@@@@smithgmail.com")

class TestUser(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation_without_role(self):
        print "test_user_creation_without_role"
        with self.assertRaises(AttributeRequired):
            user = User(name=Name("Robin Smith"),
                            email=Email("smith@gmail.com"))

    def test_user_creation_with_role(self):
        print "test_user_creation_with_role"
        role = Role(name=Name("admin"))
        role.save()
        user = User(name=Name("Robin Smith"),
                    email=Email("smith@gmail.com"),
                    role=Role.get_by_id(1))
        user.save()
        self.assertEqual(user.role.name, "admin")

    def test_set_toles_to_user(self):
        print "test_set_toles_to_user"
        role = Role(name=Name("admin"))
        role.save()
        user = User(name=Name("Robin Smith"),
                    email=Email("smith@gmail.com"),
                    role=Role.get_by_id(1))
        user.save()
        role = Role(name=Name("user"))
        user.set_role(role)
        user.save()
        users = User.get_all()
        self.assertEqual(users[0].role.name, "user")

    def test_user_get_all(self):
        print "test_user_get_all"
        role = Role(name=Name("Admin"))
        role.save()
        user = User(name=Name("Termite"),
                    email=Email("tremite@gmail.com"),
                    role=role)
        user.save()
        users = User.get_all()
        self.assertEqual("Admin", users[0].role.name)

    def test_get_user_by_id(self):
        print "test_get_user_by_id"
        user = User(name=Name("Robin Smith"),
                    email=Email("smith@gmail.com"),
                    role=Role(name=Name("admin")))
        user.save()
        self.assertEqual(user.get_by_id(1).role.name, "admin")
        self.assertEqual(user.get_by_id(1).name, "Robin Smith")

    def test_update_user(self):
        print "test_update_role"
        user = User(name=Name("Robin Smith"),
                    email=Email("smith@gmail.com"),
                    role=Role(name=Name("admin")))
        user.save()
        u1 = User.get_by_id(1)

        u1.update(name=Name("Duddley Rod"),
                  email=Email("duddley@gmail.com"),
                  role=Role(name=Name("owner")))

        self.assertEqual(u1.get_by_id(1).name, "Duddley Rod")
        self.assertEqual(u1.get_by_id(1).role.name, "owner")

class TestRole(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_role_creation(self):
        print "test_role_creation"
        role = Role(name=Name("admin"))
        role.save()
        self.assertEqual(role.name, "admin")

    def test_role_set_name(self):
        print "test_role_set_name"
        role = Role(name=Name("admin"))
        role.save()
        role.set_name(Name("owner"))
        role.save()
        role = Role.get_by_id(1)
        self.assertEqual(role.name, "owner")

    def test_set_users_to_role(self):
        print "test_set_users_to_role"

    def test_get_role_by_id(self):
        print "test_get_role_by_id"
        role = Role(name=Name("Admin"))
        role.save()
        self.assertEqual(role.get_by_id(1).name, "Admin")

    def test_update_role(self):
        print "test_update_role"
        role = Role(name=Name("Admin"))
        role.save()
        rl = Role.get_by_id(1)
        rl.update(name=Name("owner"))
        self.assertEqual(rl.get_by_id(1).name, "owner")

    def test_role_get_all(self):
        print "test_role_get_all"
        role = Role(name=Name("Admin"))
        role.save()
        roles = Role.get_all()
        self.assertEqual("Admin", roles[0].name)

class TestSession(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_session_creation(self):
        print "session creation testing"
        role = Role(name=Name('admin'))
        role.save()
        user = User(name = Name('johns'),email = Email('johnsn@gmail.com'), role = Role.get_by_id(1));
        user.save()
        sess = Session(user);
        self.assertEqual(sess.get_user(),user);

class TestSystem(TestCase):

    from src.db import sys

    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        ar = Role(name = Name('admin'))
        ur = Role(name = Name('user'))
        ar.save()
        ur.save()
        user1 = User(name= Name('john'), email= Email('john@gmail.com') , role= Role.get_by_id(1) )
        user2 = User(name= Name('johnsnow'), email = Email('johnsnow@gmail.com') , role =Role.get_by_id(2) )
        user1.save()
        user2.save()
        sessi = Session(user1)
        sessi1 = Session(user2)
        global sys
        sys.session_list.append(sessi)
        sys.session_list.append(sessi1)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        global sys
        sys.session_list = []

    def test_adduser(self):
        print 'testing System: adduser'
        global sys
        user3 = User(name = Name('raju'),email = Email('ra@man.com'),role = Role.get_by_id(1) )
        user3.save()
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
#        list_t = User.get_all()
#        for i in range(0,len(list_t)):
#            print list_t[i].email
        with self.assertRaises(ConstraintError): # trying to add same user
            sys.add_user(normal_logged[0].get_user(),admin_logged[0])
        with self.assertRaises(ConstraintError): # normal uesr trying to add user
            user2  = User(name= Name('raj'), email= Email('raj@gmail.com') , role = Role.get_by_id(1))
            user2.save();
            sys.add_user(user2,normal_logged[0])
        with self.assertRaises(ConstraintError): # proper instances not passed
            user2 = User(name= Name('rajman'), email= Email('rajman@gmail.com') , role = Role.get_by_id(2))
            user2.save()
            sys.add_user(admin_logged[0],user2)



    def test_showusers(self):
        print 'testing System: show_users'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]

        a = sys.show_users(admin_logged[0])
        print 'rajman'
        print len(a)
        for i in range(0,len(a)):
            self.assertEqual(str(a[i].get_email()),str(User.get_all()[i].get_email()))
            self.assertEqual(str(a[i].get_name()),str(User.get_all()[i].get_name()))

    def test_deluser(self):
        print 'testing System: del_users'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        with self.assertRaises(ConstraintError): # normal user trying to delete user
            user2 = User(name= Name('raj'), email= Email('raj@gmail.com') , role= Role.get_by_id(2) )
            user2.save()
            sys.users.append(user2)
            sys.del_user(user2,normal_logged[0])
        with self.assertRaises(ConstraintError): # you cannot delete an admin
            user3 = User(name= Name('raja'), email= Email('raja@gmail.com') , role= Role.get_by_id(1))
            user3.save()
            sys.users.append(user3)
            sys.del_user(user3,admin_logged[0])
        with self.assertRaises(ConstraintError): # cannot delete oneself
            sys.del_user(admin_logged[0].get_user(),admin_logged[0])

    def test_getuserbyemail(self):
        print 'testing System: get_user by email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        print 'raj'
        print len(admin_logged)
        a = sys.getUserByEmail(Email('john@gmail.com'),admin_logged[0])
        self.assertEqual(a[0].get_name(),'john')
        self.assertEqual(len(a),1)
        self.assertEqual(a[0].get_email(),'john@gmail.com')

    def test_getemail(self):
        print 'testing System: get_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        a = sys.get_email(normal_logged[0].get_user(),admin_logged[0])
        self.assertEqual(a,'johnsnow@gmail.com')

    def test_getname(self):
        print 'testing System: get_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        a = sys.get_name(normal_logged[0].get_user(),admin_logged[0])
        self.assertEqual(a,'johnsnow')

    def test_getemail(self):
        print 'testing System: get_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        a = sys.get_role(admin_logged[0].get_user(),admin_logged[0])
        self.assertEqual(a,Role.get_by_id(1))

    def test_setemail(self):
        print 'testing System: set_email'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        sys.set_email(normal_logged[0].get_user(),Email('johnraj@gmail.com'),admin_logged[0]) # admin changing
        self.assertEqual(normal_logged[0].get_user().get_email(),'johnraj@gmail.com')
        self.assertEqual(sys.getUserByEmail(Email('johnraj@gmail.com'),admin_logged[0])[0],normal_logged[0].get_user())
        sys.set_email(normal_logged[0].get_user(),Email('johnsnow@gmail.com'),admin_logged[0]) # user changing bakc
        self.assertEqual(normal_logged[0].get_user().get_email(),'johnsnow@gmail.com')
        self.assertEqual(sys.getUserByEmail(Email('johnsnow@gmail.com'),admin_logged[0])[0],normal_logged[0].get_user())

    def test_setname(self):
        print 'testing System: set_name'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        sys.set_name(normal_logged[0].get_user(),Name('johnraj'),admin_logged[0]) # admin changing
        self.assertEqual(normal_logged[0].get_user().get_name(),'johnraj')
        sys.set_name(normal_logged[0].get_user(),Name('johnsnow'),normal_logged[0]) # user changing bakc
        self.assertEqual(normal_logged[0].get_user().get_name(),'johnsnow')

    def test_showsessions(self):
        print 'testing System: show session'
        global sys
        admin_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(1)]
        normal_logged = [s for s in sys.session_list if s.get_user().get_role()==Role.get_by_id(2)]
        with self.assertRaises(ConstraintError):
            a = sys.showSessions(normal_logged[0])
        b = sys.showSessions(admin_logged[0])
        for i in range(0,len(b)):
            self.assertEqual(str(b[i].get_user().get_email()),str(sys.session_list[i].get_user().get_email()))
            self.assertEqual(str(b[i].get_user().get_name()),str(sys.session_list[i].get_user().get_name()))
            self.assertEqual(str(b[i].get_user().get_role()),str(sys.session_list[i].get_user().get_role()))



if __name__ == '__main__':
    unittest.main()
