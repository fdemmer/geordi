"""A Django middleware for interactive profiling"""

import cProfile
import marshal
import socket
import subprocess
import tempfile

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

from django.template.loader import render_to_string

__all__ = ['HolodeckException', 'VisorMiddleware']

class HolodeckException(Exception):
    """Captain, the holodeck's malfunctioning again!"""

class VisorMiddleware(object):
    """Interactive profiling middleware.

    When a request comes in that has a __geordi__ GET parameter, this bypasses
    the view function, profiles the request, and returns the profiler output.

    Note that this only runs if settings.DEBUG is True or if the current user
    is a super user.
    """
    def __init__(self, app=None, allowedfunc=None):
        self._app = app
        if allowedfunc is not None:
            self._allowed = allowedfunc

    def _response(self, profiler):
        profiler.create_stats()

        with tempfile.NamedTemporaryFile(prefix='geordi-', suffix='.pstats'
                                         ) as stats:
            stats.write(marshal.dumps(profiler.stats))
            stats.flush()

            p = subprocess.Popen(['gprof2dot', '-f', 'pstats', stats.name],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.close()
            output = p.stdout.read()
            retcode = p.wait()
            if retcode:
                raise HolodeckException('gprof2dot exited with %d'
                                        % retcode)

            body = str(render_to_string('geordi/geordi.html',
                                        {'dotstring': output}).encode('utf-8'))
            headers = [('Content-Type', 'text/html; charset=utf-8'),
                       ('X-Geordi-Served-By', socket.gethostname()),
                       ('Content-Length', str(len(body)))]

            return headers, body

    def _allowed(self, environ):
        qs = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
        return '__geordi__' in qs

    def __call__(self, environ, start_response):
        if not self._allowed(environ):
            return self._app(environ, start_response)

        def dummy_start_response(status, response_headers, exc_info=None):
            pass

        profiler = cProfile.Profile()
        profiler.runcall(self._app, environ, dummy_start_response)
        headers, output = self._response(profiler)
        start_response('200 OK', headers)
        return [output]

    def _djangoallowed(self, request):
        """Return whether or not the middleware should run"""
        from django.conf import settings
        if settings.DEBUG:
            return True

        user = getattr(request, 'user', None)
        if user is not None:
            return user.is_superuser
        else:
            return False

    def process_request(self, request):
        if ('__geordi__' not in request.GET or
            not self._djangoallowed(request)):
            return

        request._geordi = cProfile.Profile()
        request._geordi.enable()

    def process_response(self, request, response):
        profiler = getattr(request, '_geordi', None)
        if profiler is None:
            return response

        profiler.disable()
        headers, output = self._response(profiler)

        from django.http import HttpResponse
        profresponse = HttpResponse(output)
        for name, value in headers:
            profresponse[name] = value
        return profresponse
