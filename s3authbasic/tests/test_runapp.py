import os
import unittest

from s3authbasic.runapp import main
from s3authbasic.testing import unset_environment

environ = {
    'USER_admin': '8c6976e5b5410415bde908bd4dee15dfb16',
    'AWS_BUCKET_NAME': 'bucket_example',
    'AWS_ACCESS_KEY_ID': '123123',
    'AWS_SECRET_ACCESS_KEY': '123123123',
}


def mock_serve(app, host='0.0.0.0', port='6543', url_scheme='http'):
    return {
        'app': app,
        'host': host,
        'port': port,
        'url_scheme': url_scheme,
    }


class RunAppTest(unittest.TestCase):

    def setUp(self):
        os.environ.update(environ)

    def test_default_run(self):
        app = main(serve=mock_serve)
        self.assertTrue(app['host'] == '0.0.0.0')

    def test_change_port(self):
        os.environ.update({
            'PORT': '9999'
        })
        app = main(serve=mock_serve)
        self.assertTrue(app['port'] == 9999)

    def test_change_scheme(self):
        app = main(serve=mock_serve)
        self.assertTrue(app['url_scheme'] == 'https')
        os.environ.update({
            'SCHEME': 'http'
        })
        app = main(serve=mock_serve)
        self.assertTrue(app['url_scheme'] == 'http')

    def test_change_settings(self):
        os.environ.update({
            'SETTINGS': 's3authbasic/config-templates/production.ini'
        })
        app = main(serve=mock_serve)
        self.assertTrue(app['url_scheme'] == 'http')

    def tearDown(self):
        unset_environment()
