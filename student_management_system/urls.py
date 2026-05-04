from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import views
from student_management_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin', views.doLogin, name="do_login"),
    path('', views.ShowLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),

    # Per-role URL modules
    path('', include('base.hod_urls')),
    path('', include('base.staff_urls')),
    path('', include('base.student_urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                             document_root=settings.
                                                                             STATIC_ROOT)
