from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls', namespace='user')),
    path('api/loan/', include('core.urls', namespace='core'))
]
