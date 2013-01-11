# ---------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011-2013 Yellowem Inc
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------

from django.conf.urls.defaults import patterns, url, include
from tastypie.api import Api

from ultra_blog.api import BlogResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(BlogResource())


urlpatterns = patterns('',
        (r'^api/', include(v1_api.urls)),
        url(r'^register/$', "ultra_blog.views.register.index",
            name="register-view"),
        url(r'^$', "ultra_blog.views.home.index",
            name="home"),
)
