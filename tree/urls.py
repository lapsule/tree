"""tree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls import re_path
from django.contrib import admin
from filebrowser.sites import site
from django.contrib.auth.models import User
from django.urls import include, path
from area.views import tree

from area.models import Area


from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = ('url', 'name', 'alias', 'common_level')

# ViewSets define the view behavior.
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer



# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'areas', AreaViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tree/', tree),
    # path('api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'admin/filebrowser/', site.urls),
    url('grappelli/', include('grappelli.urls')),  # grappelli URLS
]
