from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', lambda req: HttpResponse('OK')),
]
