import os
from hashlib import sha256

from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import Allow, Authenticated


def check_credentials(username, password, request):
    credentials = request.registry.settings['credentials']
    passwordhash = credentials.get(username, None)

    passwordhashed = sha256(password).hexdigest()
    if passwordhash is not None and passwordhashed == passwordhash:
        return [username]


def read_settings(settings, key, default=None):
    env_key = key.upper()
    if env_key in os.environ:
        return os.environ.get(env_key)
    else:
        return settings.get(key, default)


def read_users(settings):
    credentials = {}
    key_prefix = 'user_'

    for key in settings.keys():
        if key.startswith(key_prefix):
            username = key.replace(key_prefix, '')
            password = settings.get(key)
            credentials[username] = password

    for key in os.environ.keys():
        if key.startswith(key_prefix):
            username = key.replace(key_prefix, '')
            password = os.environ.get(key)
            credentials[username] = password

    return credentials


class RootSite(object):
    __acl__ = [
        (Allow, Authenticated, 'view'),
    ]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['credentials'] = read_users(settings)
    settings['realm'] = read_settings(settings, 'realm',
                                      default='Protected site')

    authn_policy = BasicAuthAuthenticationPolicy(check_credentials,
                                                 realm=settings['realm'],
                                                 debug=True)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          root_factory=RootSite)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
