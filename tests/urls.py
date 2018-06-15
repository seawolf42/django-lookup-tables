from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from rest_framework.routers import DefaultRouter

from sample_app import views


router = DefaultRouter()
router.register(r'mymodels', views.MyModelViewSet, base_name='mymodel')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include((router.urls, 'sample_app'), namespace='api')),
    url(r'^$', lambda req: HttpResponse('OK')),
]
