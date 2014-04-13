import os

from paste.deploy import loadapp
from waitress import serve


def main(serve=serve):
    port = int(os.environ.get("PORT", 6543))
    scheme = os.environ.get("SCHEME", "https")
    if 'SETTINGS' in os.environ:
        settings = os.environ.get("SETTINGS")
        app = loadapp('config:' + settings)
    else:
        app = loadapp('config:production.ini',
                      relative_to='s3authbasic/config-templates')
    return serve(app, host='0.0.0.0', port=port, url_scheme=scheme)
