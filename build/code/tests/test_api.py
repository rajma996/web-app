
# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
from datetime import datetime
# import json

from src.db import *
from src.app import create_app
from src.op_exceptions import AttributeRequired

config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

from src.db import sys

from src.db import sys
class TestUser(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        sys.session_list = []
        db.drop_all()

    def test_get_all_users(self):
        print "test_get_all_users"
        global sys
        ###Create Users
        role1 = Role(name=Name("admin"))
        role1.save()
        role2 = Role(name=Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=role1)
        user1.save()
        user2 = User(name=Name("normal user"),
                    email=Email("normal@xyz.com"),
                    role=role2)
        user2.save()

        login_user(user2,sys)
        login_user(user1,sys)

        headers = {'content-type': 'application/json' , 'session' : 'admin@xyz.com'}

        response = self.client.get("/users",headers=headers)

        self.assertEqual(response.status_code, 200)


    def test_get_one_user(self):

        print "test_get_one_user"

        ### create a User
        role1 = Role(name=Name("admin"))
        role1.save()
        role2 = Role(name=Name("user"))
        role2.save()

        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=role1)
        user1.save()
        user2 = User(name=Name("normal user"),
                    email=Email("normal@xyz.com"),
                    role=role2)
        user2.save()

        r = self.client.get('/users/1')
        result = json.loads(r.data)
        self.assertEqual(result['name'], "admin user")

    def test_update_existing_user(self):

        # Create a user
        # update the same user
        role1 = Role(name=Name("admin"))
        role1.save()
        role2 = Role(name=Name("user"))
        role2.save()

        user1 = User(name=Name("admin user"),
                     email=Email("admin@xyz.com"),
                     role=role1)

        user1.save()
        login_user(user1,sys)


        user2 = User(name=Name("normal user"),
                     email=Email("normal@xyz.com"),
                     role=role2)

        user2.save()

        payload = {'email': 'ttt@kkk.com',
                   'name': 'nearly normal',
                   'session': 'admin@xyz.com'}

        headers = {'content-type': 'application/json' , 'session' : 'admin@xyz.com'}

        response = self.client.put("/users/2",
                                   data=json.dumps(payload),
                                   headers=headers)


        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):

        print "test_create_new_user"
        role1 = Role(name=Name("admin"))
        role1.save()
        role2 = Role(name=Name("user"))
        role2.save()

        user1 = User(name=Name("admin user"),
                     email=Email("admin@xyz.com"),
                     role=role1)
        user1.save()

        login_user(user1,sys)

        user2 = User(name=Name("normal user"),
                     email=Email("normal@xyz.com"),
                     role=role2)


        user2.save()

        payload = {'email': 'ttt@kkk.com',
                   'name': 'nearly normal user',
                   'role' : 'user',
                   'session': 'admin@xyz.com'}

        headers = {'content-type': 'application/json' , 'session' : 'admin@xyz.com'}

        response = self.client.post("/users/",
                                    data=json.dumps(payload),
                                    headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):

        print "test_delete_user"
        role1 = Role(name=Name("admin"))
        role1.save()
        role2 = Role(name=Name("user"))
        role2.save()

        user1 = User(name=Name("admin user"),
                     email=Email("admin@xyz.com"),
                     role=role1)

        user1.save()

        login_user(user1,sys)

        user2 = User(name=Name("normal user"),
                     email=Email("normal@xyz.com"),
                     role=role2)

        user2.save()

        login_user(user2,sys);

        user3 = User(name=Name("normal userraj"),
                     email=Email("normal2@xyz.com"),
                     role=role2)

        user3.save()

        headers = {'content-type': 'application/json' , 'session': 'normal2@xyz.com'}

        response = self.client.delete("/users/3",headers=headers)

        self.assertEqual(response.status_code, 500) # normal user cannot delete a user

        headers = {'content-type': 'application/json' , 'session': 'admin@xyz.com'}

        response = self.client.delete("/users/3",headers=headers)

        self.assertEqual(response.status_code, 200) # admin user can delete a user

if __name__ == '__main__':
    unittest.main()
