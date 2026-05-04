import logging

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        logger.debug("Module accessed: %s by user: %s", modulename, getattr(request.user, 'username', 'anonymous'))
        user = request.user
        if user.is_authenticated:
            user_type = str(user.user_type)
            if user_type == "1":
                if modulename == "base.HodViews":
                    pass
                elif modulename == "base.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user_type == "2":
                if modulename == "base.StaffViews" or modulename == "base.EditResultVIewClass":
                    pass
                elif modulename == "base.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user_type == "3":
                if modulename == "base.StudentViews" or modulename == "django.views.static":
                    pass
                elif modulename == "base.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse(
                    "do_login") or modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites" or modulename == "base.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
