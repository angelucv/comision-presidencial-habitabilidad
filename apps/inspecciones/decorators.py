from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.cuentas.inspectores import usuario_es_inspector_certificado


def inspector_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not usuario_es_inspector_certificado(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper
