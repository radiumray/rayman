"""rayman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import view
from . import testdb
from . import search

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^$', view.hello),
    url('base/', view.base),
    url('hello/', view.hello),
    url('^addToDB/', testdb.addToDB),
    url('^queryFromDB/', testdb.queryFromDB),
    url('^updateToDB/', testdb.updateToDB),
    url('^deleteToDB/', testdb.deleteToDB),
    url('^search-form/', search.search_form),
    url('^search/', search.search),

    url('^addUser/', testdb.addToDBForm),

    # (r'^postSearch/$', postSearch.search_post),
    # url(r'^search-form/$', search.search_form),
    # url(r'^search/$', search.search),

]
