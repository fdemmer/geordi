import os
import webbrowser

from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

from geordi import VisorMiddleware

app = None
settings.configure(DEBUG=True,
                   WSGI_APPLICATION='geordi.shell.app',
                   INSTALLED_APPS=['django.contrib.staticfiles', 'geordi'],
                   STATIC_URL='/',
                   ROOT_URLCONF='django.contrib.staticfiles.urls',
                   MIDDLEWARE_CLASSES=[])


def execute_and_serve(prog):
    global app
    wsgi = get_wsgi_application()

    def allowed(environ):
        return environ['PATH_INFO'] == '/'

    def app_(environ, start_response):
        if allowed(environ):
            with open(prog, 'rb') as f:
                code = compile(f.read(), prog, 'exec')
            globs = {'__file__': prog,
                     '__name__': '__main__',
                     '__package__': None}

            eval(code, globs)
        else:
            return wsgi(environ, start_response)

    app = VisorMiddleware(app_, allowedfunc=allowed)
    os.environ['RUN_MAIN'] = 'true'
    webbrowser.open('http://localhost:41000')
    return execute_from_command_line(
        ['django-admin', 'runserver', '--noreload', '--nostatic',
         '0.0.0.0:41000'])
