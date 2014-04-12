from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import forget
from pyramid.view import view_config, forbidden_view_config


@forbidden_view_config()
def basic_challenge(request):
    response = HTTPUnauthorized()
    response.headers.update(forget(request))
    return response


@view_config(route_name='home', renderer='templates/mytemplate.pt',
             permission='view')
def my_view(request):
    return {'project': 's3authbasic'}
