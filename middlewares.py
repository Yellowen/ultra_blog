# ---------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011-2013 Sameer Rahmani <lxsameer@gnu.org>
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

import datetime
import urllib
import logging

from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.signals import user_logged_in
from django.utils import translation

from ultra_blog.models import BlogAlias


logger = logging.getLogger('django')


class HttpResponseRedirectAuth(HttpResponsePermanentRedirect):
    pass


class BlogMiddleware(object):
    """
    This middleware get the current domain and set the suitable object on
    request.
    """

    def process_request(self, request):
        global_domain = True
        try:
            blogalias = BlogAlias.objects.get(domain=request.META['HTTP_HOST'])
            global_domain = False
            blog = blogalias.blog
            setattr(request, "blog", blog)
            setattr(request, "domain", blogalias)

            # Setup blog language
            translation.activate(blog.language)
            request.LANGUAGE_CODE = translation.get_language()

        except BlogAlias.DoesNotExist:
            blogalias = None
            setattr(request, "urlconf", "yblog.global_urls")
            setattr(request, "blog", None)
            setattr(request, "domain", request.META['HTTP_HOST'])

        setattr(request, "is_global", global_domain)
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_response(self, request, response):
        return response
