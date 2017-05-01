======================================
 Geordi: Interactive Django profiling
======================================

Geordi is a `Django`_ `middleware`_ that lets you interactively profile your
site. Add ``?__geordi__`` to any URL, browse to it, and you'll get an
interactive call graph of the request's code path and the time spent in each
function.

If you've set ``DEBUG = True`` in your `Django settings`_, anyone can profile
a page–even anonymous users. With ``DEBUG = False``, only super users can
profile pages.

.. _Django: https://www.djangoproject.com/
.. _middleware: https://docs.djangoproject.com/en/dev/topics/http/middleware/
.. _Django settings: https://docs.djangoproject.com/en/dev/topics/settings/


Installation
------------

After you've done ``pip install geordi``, add ``'geordi'`` to the
``INSTALLED_APPS`` setting, and add ``'geordi.VisorMiddleware'`` to the
``MIDDLEWARE_CLASSES`` setting. You'll probably want to put it after Django's
authentication middleware and before everything else.
