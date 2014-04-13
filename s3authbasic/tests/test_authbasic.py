from s3authbasic.testing import BaseAppTest, AUTH_ENVIRON


class AuthBasicTests(BaseAppTest):

    def test_valid_credentials(self):
        self.testapp.get('/', extra_environ=AUTH_ENVIRON, status=200)

    def test_not_valid_credentials(self):
        self.testapp.get('/', extra_environ={
            'HTTP_AUTHORIZATION': 'Basic NOTVALIDPASS='
        }, status=401)

    def test_not_credentials(self):
        self.testapp.get('/', status=401)
