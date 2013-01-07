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
import re

from django.shortcuts import render_to_response as rr
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.conf import settings

from ultra_blog.forms import RegisterBlogForm
from ultra_blog.base import ClassView
from ultra_blog.models import Blog, BlogAlias


class RegisterBlog(ClassView):
    """
    Register view.
    """

    #: Address of default template of view
    template = "ultra_blog/register.html"

    #: Address of template for registeration completion
    done_template = "ultra_blog/register_done.html"

    #: Is it a global view ?
    is_global = True

    #: Page title
    title = "Yellowers.com | Register"

    #: Blog Registeration form 
    Form = RegisterBlogForm
    
    def on_get(self, request):
        """
        On GET request.
        """
        form = self.Form()
        self.context["form"] = form
        return self.rr()

    def on_post(self, request):
        """
        On Post request.
        """
        form = self.Form(request.POST)

        if form.is_valid():
            # If form is valid, (invitation code)
            code = form.cleaned_data["code"]
            domain = form.cleaned_data["name"].lower()
            lang = form.cleaned_data["lang"]
            try:
                site = BlogAlias.objects.get(domain=domain)
                form.errors["name"] = [_("This domain is not available")]

            except BlogAlias.DoesNotExist:
                # Every thing is ok
                # Create the blog entry
                blog = Blog(founder=request.user)
                blog.language = lang
                blog.save()
                blog.authors.add(request.user)
                blog.save()
                
                # Create block alias
                subdomain = "%s.%s" % (domain,
                                       settings.DOMAIN)
                
                alias = BlogAlias(domain=subdomain,
                                  blog=blog)
                alias.save()
                
                # expire the invitation code
                code.blog = blog
                code.active = False
                code.save()
                
                # Show the done view
                return self.done(request, blog)

        self.context["form"] = form
        return self.rr()

    def done(self, request, blog):
        self.context["blog"] = blog
        return self.rr(template=self.done_template)


index = RegisterBlog()
