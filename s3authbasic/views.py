from pyramid.httpexceptions import HTTPUnauthorized, HTTPNotFound
from pyramid.security import forget
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config


@forbidden_view_config()
def basic_challenge(request):
    response = HTTPUnauthorized()
    response.headers.update(forget(request))
    return response


@view_config(route_name='site', permission='view')
def site(request):
    s3file = request.s3.get_file(request.path)
    if s3file is None:
        return HTTPNotFound()
    response = Response(content_type='text/html')
    response.app_iter = s3file
    return response
