import unittest
import os
from s3authbasic import main
from s3authbasic.testing import S3ConnectionMockup
from pyramid.exceptions import ConfigurationError


class SettingsFile(unittest.TestCase):

    def test_correct_settings(self):
        settings = {
            'user_admin': '8c6976e5b5410415bde908bd4dee15dfb16'
                          '7a9c873fc4bb8a81f6f2ab448a918',
            'aws_bucket_name': 'bucket_example',
            'aws_access_key_id': '123123',
            'aws_secret_access_key': '123123123',
            'S3Wrapper': S3ConnectionMockup,
        }

        main({}, **settings)

    def test_not_aws_vars(self):
        settings = {
            'user_admin': '8c6976e5b5410415bde908bd4dee15dfb16'
                          '7a9c873fc4bb8a81f6f2ab448a918',
            'S3Wrapper': S3ConnectionMockup,
        }

        self.assertRaises(ConfigurationError, main, {}, **settings)

    def test_not_users(self):
        settings = {
            'aws_bucket_name': 'bucket_example',
            'aws_access_key_id': '123123',
            'aws_secret_access_key': '123123123',
            'S3Wrapper': S3ConnectionMockup,
        }

        self.assertRaises(ConfigurationError, main, {}, **settings)


class EnvironSettings(unittest.TestCase):

    settings = {
        'S3Wrapper': S3ConnectionMockup,
    }

    def test_correct_settings(self):
        environ = {
            'USER_admin': '8c6976e5b5410415bde908bd4dee15dfb16',
            'AWS_BUCKET_NAME': 'bucket_example',
            'AWS_ACCESS_KEY_ID': '123123',
            'AWS_SECRET_ACCESS_KEY': '123123123',
        }

        os.environ.update(environ)

        main({}, **self.settings)

    def test_not_aws_vars(self):
        environ = {
            'USER_admin': '8c6976e5b5410415bde908bd4dee15dfb16',
        }

        os.environ.update(environ)

        self.assertRaises(ConfigurationError, main, {}, **self.settings)

    def test_not_users(self):
        environ = {
            'AWS_BUCKET_NAME': 'bucket_example',
            'AWS_ACCESS_KEY_ID': '123123',
            'AWS_SECRET_ACCESS_KEY': '123123123',
        }

        os.environ.update(environ)

        self.assertRaises(ConfigurationError, main, {}, **self.settings)

    def tearDown(self):
        for item in [
            'USER_admin',
            'AWS_BUCKET_NAME',
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
        ]:
            if item in os.environ:
                del os.environ[item]
