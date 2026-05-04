import logging
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


def hod_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/')
    def wrapper(request, *args, **kwargs):
        if str(request.user.user_type) != "1":
            logger.warning("Non-HOD user %s attempted to access %s", request.user.username, request.path)
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/')
    def wrapper(request, *args, **kwargs):
        if str(request.user.user_type) != "2":
            logger.warning("Non-Staff user %s attempted to access %s", request.user.username, request.path)
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/')
    def wrapper(request, *args, **kwargs):
        if str(request.user.user_type) != "3":
            logger.warning("Non-Student user %s attempted to access %s", request.user.username, request.path)
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return wrapper
