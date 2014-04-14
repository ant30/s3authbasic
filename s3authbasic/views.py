import sys

from pyramid.httpexceptions import HTTPUnauthorized, HTTPNotFound
from pyramid.security import forget
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config


if sys.version_info[0] < 3:
    from urllib2 import unquote
else:
    from urllib.parse import unquote


@forbidden_view_config()
def basic_challenge(request):
    response = HTTPUnauthorized()
    response.headers.update(forget(request))
    return response


@view_config(route_name='site', permission='view')
def site(request):
    path = unquote(request.path)
    s3file = request.s3.get_file(path)
    if s3file is None:
        return HTTPNotFound()
    response = Response(content_type=s3file.content_type)
    response.app_iter = s3file
    return response
