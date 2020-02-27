import unittest

from flask import abort, url_for
from flask_testing import TestCase

from application import app, db
from application.models import Users, Posts

class TestBase(TestCase):

    def create_app(self):

        # pass in configurations for test database
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://alina:password@127.0.0.1/dbtest')
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # ensure there is no data in the test database when the test starts
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_posts_view(self):
        """
        Test that account page isn't accessible without login
        """
        response = self.client.get(url_for('account'))
        self.assertEqual(response.status_code, 302)

    def test_post_redirect(self):
        """
	Test that login redirects to correct page if user accesses /post
	"""
        target_url = url_for('post')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertRedirects(response, redirect_url)
    def test_user_db(self):
        """
        Test that the user is in the db correctly and password is hashed
        """
        admin = Users.query.filter_by(first_name='admin').first()
        employee = Users.query.filter_by(first_name='test').first()
        self.assertTrue(admin)
        self.assertTrue(employee)
        assert admin.password != 'test123'
        assert employee.password != 'anothertest123'    
