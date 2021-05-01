from __future__ import absolute_import, unicode_literals

import inspect

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register
from django.middleware.gzip import GZipMiddleware
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _


class DebugToolbarConfig(AppConfig):
    name = 'debug_toolbar'
    verbose_name = _("Debug Toolbar")


@register
def check_middleware(app_configs, **kwargs):
    from debug_toolbar.middleware import DebugToolbarMiddleware

    errors = []
    gzip_index = None
    debug_toolbar_index = None

    setting = getattr(settings, 'MIDDLEWARE', None)
    setting_name = 'MIDDLEWARE'
    if setting is None:
        setting = settings.MIDDLEWARE_CLASSES
        setting_name = 'MIDDLEWARE_CLASSES'

    # Determine the indexes which gzip and/or the toolbar are installed at
    for i, middleware in enumerate(setting):
        if is_middleware_class(GZipMiddleware, middleware):
            gzip_index = i
        elif is_middleware_class(DebugToolbarMiddleware, middleware):
            debug_toolbar_index = i

    if debug_toolbar_index is None:
        # If the toolbar does not appear, report an error.
        errors.append(
            Error(
                "debug_toolbar.middleware.DebugToolbarMiddleware is missing "
                "from %s." % setting_name,
                hint="Add debug_toolbar.middleware.DebugToolbarMiddleware to "
                "%s." % setting_name,
            )
        )
    elif gzip_index is not None and debug_toolbar_index < gzip_index:
        # If the toolbar appears before the gzip index, report an error.
        errors.append(
            Error(
                "debug_toolbar.middleware.DebugToolbarMiddleware occurs before "
                "django.middleware.gzip.GZipMiddleware in %s." % setting_name,
                hint="Move debug_toolbar.middleware.DebugToolbarMiddleware to "
                "after django.middleware.gzip.GZipMiddleware in %s." % setting_name,
            )
        )

    return errors


def is_middleware_class(middleware_class, middleware_path):
    try:
        middleware_cls = import_string(middleware_path)
    except ImportError:
        return
    return (
        inspect.isclass(middleware_cls) and
        issubclass(middleware_cls, middleware_class)
    )
