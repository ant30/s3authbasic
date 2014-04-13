from mimetypes import MimeTypes
import os
from os import path
import urllib

import unittest
from webtest import TestApp

from . import main


BASEPATH = path.abspath(path.dirname(__file__))
FIXTURES = path.join(BASEPATH, 'tests/fixtures')

AUTH_ENVIRON = {
    'HTTP_AUTHORIZATION': 'Basic YWRtaW46YWRtaW4='
}


class S3FileMockup(object):

    def __init__(self, filepath, block_size=1024):
        mime = MimeTypes()
        self.block_size = block_size
        url = urllib.pathname2url(filepath)
        self.content_type = mime.guess_type(url)[0]
        self.file = open(filepath)

    def __iter__(self):
        return self

    def next(self):
        val = self.file.read(self.block_size)
        if not val:
            raise StopIteration
        return val

    #  py3
    __next__ = next

    def close(self):
        self.file.close()


class S3BucketMockup:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.abspath = path.join(FIXTURES, bucket_name)

    def lookup(self, filename):
        if filename.startswith('/'):
            filename = filename[1:]

        file = path.join(self.abspath, filename)
        if path.isfile(file):
            return S3FileMockup(file)
        return None


class S3ConnectionMockup:

    def __init__(self, key, secret):
        self.key_id = key
        self.key_secret = secret

    def get_bucket(self, bucket_name, validate=True):
        return S3BucketMockup(bucket_name)


def unset_environment():
    for item in [
        'USER_admin',
        'AWS_BUCKET_NAME',
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
    ]:
        if item in os.environ:
            del os.environ[item]


class BaseAppTest(unittest.TestCase):

    def setUp(self):
        unset_environment()
        settings = {
            'user_admin': '8c6976e5b5410415bde908bd4dee15dfb16'
                          '7a9c873fc4bb8a81f6f2ab448a918',
            'aws_bucket_name': 'bucket_example',
            'aws_access_key_id': '123123',
            'aws_secret_access_key': '123123123',
            'S3Wrapper': S3ConnectionMockup,
        }

        app = main({}, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        unset_environment()
        self.testapp.reset()
