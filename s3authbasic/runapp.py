import os
from os import path

from paste.deploy import loadapp
from waitress import serve

PACKAGE_DIR = path.abspath(path.dirname(__file__))


def main(serve=serve):
    port = int(os.environ.get("PORT", 6543))
    scheme = os.environ.get("SCHEME", "https")
    if 'SETTINGS' in os.environ:
        settings = os.environ.get("SETTINGS")
        app = loadapp('config:' + settings, relative_to='.')
    else:
        app = loadapp('config:production.ini',
                      relative_to=path.join(PACKAGE_DIR,
                                            'config-templates'))
    return serve(app, host='0.0.0.0', port=port, url_scheme=scheme)
