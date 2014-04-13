import os
from hashlib import sha256

from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.security import Allow, Authenticated

from .s3controller import S3Controller, get_s3_controller


def check_credentials(username, password, request):
    credentials = request.registry.settings['credentials']
    passwordhash = credentials.get(username, None)

    passwordhashed = sha256(password).hexdigest()
    if passwordhash is not None and passwordhashed == passwordhash:
        return [username]


def read_settings(settings, key, default=None, required=False):
    env_key = key.upper()
    value = None
    if env_key in os.environ:
        value = os.environ.get(env_key)
    else:
        value = settings.get(key, default)

    if value is None and required:
        raise ConfigurationError('The property {0} is required'.format(key))

    return value


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

    if not credentials:
        raise ConfigurationError("There isn't any user set, please use keys"
                                 " like user_admin = 123wdsdd123123 (encoded "
                                 "via sha256)")
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

    settings['aws_bucket_name'] = read_settings(
        settings, 'aws_bucket_name', required=True)

    settings['aws_secret_access_key'] = read_settings(
        settings, 'aws_secret_access_key', required=True)

    settings['aws_access_key_id'] = read_settings(
        settings, 'aws_access_key_id', required=True)

    settings['s3'] = S3Controller(settings)

    authn_policy = BasicAuthAuthenticationPolicy(check_credentials,
                                                 realm=settings['realm'])
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          root_factory=RootSite)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_route('site', pattern='{path:.*}')
    config.add_request_method(get_s3_controller, name='s3', reify=True)

    config.scan()
    return config.make_wsgi_app()
