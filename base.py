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
import logging

from django import forms
from django.http import Http404
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.conf import settings

from models import Post


class ClassView(object):
    """
    This class is a base class for all the class views.
    """

    #: Page title
    title = ""

    #: Template file
    template = ""

    #: Specify the view scope
    is_global = True

    #: Contexts that will pass to template
    context = {}

    #: Current request object
    request = None

    @property
    def media_url(self):
        if self.is_global:
            return settings.MEDIA_URL
        else:
            template_name = self.request.blog.template
            return "%s%s/" % (settings.MEDIA_URL,
                              template_name)

    def get_template(self, request=None, template=None):
        """
        Return a suitable template path based on blog default theme.
        """
        req = request or self.request
        if self.is_global:
            return template or self.template
        else:
            template_name = req.blog.template
            return "%s/%s" % (template_name,
                              template or self.template)

    def rr(self, request=None, context={}, template=None):
        """
        Wrap around render_to_response funtion of django.
        """
        from copy import copy

        req = request or self.request
        ctx = context or self.context

        ctx["self"] = lambda: self

        return rr(self.get_template(template=template),
                  ctx,
                  context_instance=RequestContext(req))

    def index(self, request):
        """
        View method.
        """
        if not self.is_global == request.is_global:
            raise Http404()

        self.request = request

        if request.method == "POST":
            return self.on_post(request)
        else:
            return self.on_get(request)

    def on_get(self, request):
        pass

    def on_post(self, request):
        pass

    def __call__(self, *args, **kwargs):
        return self.index(*args, **kwargs)


class PostType(object):
    """
    This class act as the basic class of all types that an application provids.
    """
    name = None

    # Admin form should be a model form
    # that collect data in admin interface
    admin_form = None
    verbose_name = None

    admin_class = None

    def __unicode__(self):
        return self.verbose_name


class BlogPostTypes(object):
    """
    This class handled the post registerd by other applications.
    """
    _registery = dict()

    def __init__(self):
        self.logger = logging.getLogger()

    def register(self, type_class):
        """
        Register types class of an Vanda applications into Ultra Blog.
        """

        if not issubclass(type_class, PostType):
            raise TypeError("'%s' must be a PostType subclass." %
                            type_class)

        # Checking the provided base_class application property.
        try:
            type_name = getattr(type_class,
                                       "name").lower()
        except AttributeError:
            raise AttributeError("'%s' did not have 'name'." %
                                 type_class + ' property')

        if type_name in self._registery.keys():
            self.logger.warning("'%s' already registered." % type_name)
        else:
            self._registery[type_name] = type_class()

    def get_form(self, type_name):
        """
        Return the form of type_name
        """
        if type_name.lower() in self._registery:
            return self._registery[type_name.lower()].admin_form
        else:
            return None

    def get_type(self, type_name):
        """
        Return the type class of type_name
        """
        return self._registery[type_name.lower()]

    def get_all_admin_forms(self):
        forms = []

        admin_forms = map(lambda x: [x, self._registery[x]],
                          self._registery.keys())

        return admin_forms

    def get_types(self):
        """
        Get all of the types list.
        """
        return map(lambda x: self._registery[x].verbose_name,
                   self._registery.keys())

    def get_types_dict(self):
        """
        Get all the types in the dictionary form.
        """
        def typemap(x):
            return [self._registery[x].name,
                    self._registery[x].verbose_name]
        return [i for i in map(typemap, self._registery.keys()) if i]

    def get_types_complex(self):
        """
        Get all of the types list.
        """
        def typemap(x):
            post = Post.objects.filter(post_type_name=self._registery[x].name)
            if post:
                return [self._registery[x].name,
                        "%s (%s)" % (self._registery[x].verbose_name,
                                     post.count())]
            return None
        return [i for i in map(typemap, self._registery.keys()) if i]

post_types = BlogPostTypes()
