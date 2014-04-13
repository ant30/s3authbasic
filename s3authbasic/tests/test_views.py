from s3authbasic.testing import BaseAppTest, AUTH_ENVIRON


class AuthBasicTests(BaseAppTest):

    def test_validpath(self):
        for (path, expect) in (
            ('/', 'home'),
            ('/index.html', 'home'),
            ('/level1', 'level 1'),
            ('/level1/', 'level 1'),
            ('/level1/index.html', 'level 1'),
            ('/level1/other.html', 'other'),
            ('/level1/level2', 'level 2'),
            ('/level1/level2/index.html', 'level 2'),

        ):
            result = self.testapp.get(path, extra_environ=AUTH_ENVIRON,
                                      status=200)
            self.assertIn(expect, result.body)

    def test_not_validpath(self):
        for path in (
            '/other.html',
            '/index',
            '/level1/index',
            '/level3/',
        ):
            self.testapp.get(path, extra_environ=AUTH_ENVIRON,
                             status=404)
