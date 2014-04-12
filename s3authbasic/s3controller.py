
from boto.s3.connection import S3Connection


class S3Controller:

    def __init__(self, settings):
        self.key_id = settings['aws_access_key_id']
        self.secret = settings['aws_secret_access_key']
        self.bucket_name = settings['aws_bucket_name']

        self.s3 = S3Connection(self.key_id, self.secret)
        self.bucket = self.s3.get_bucket(self.bucket_name, validate=False)

    def get_file(self, path):
        if path == '/':
            path = 'index.html'
        s3file = self.bucket.lookup(path)
        if s3file is None:
            if not path.endswith('/'):
                path += '/'
            s3file = self.bucket.lookup(path + 'index.html')
        return s3file


def get_s3_controller(request):
    return request.registry.settings['s3']
