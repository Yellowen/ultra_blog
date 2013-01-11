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
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from ultra_blog.models import Category, Blog, BlogAlias


class UltraBlogResource(ModelResource):
    """
    Basic resource class for any blog dependent resource.
    """
    def apply_filters(self, request, applicable_filters):
        return self.get_object_list(request).filter(
            blog=request.blog,
            **applicable_filters)


class PostResource(ModelResource):
    class Meta:
        pass

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser', "is_staff"]
        authorization= Authorization()
    

class BlogResource(ModelResource):
    authors = fields.ToManyField(UserResource, "authors")

    def dehydrate(self, bundle):
        pk = bundle.data["id"]
        aliases = BlogAlias.objects.filter(blog__pk=pk)
        result = {}
        for alias in aliases:
            result.update({alias.domain: alias.pk})
        bundle.data['aliases'] = result
        return bundle

    class Meta:
        queryset = Blog.objects.all()
        filtering = {"authors": ["id", "exact"]}
        authorization= Authorization()


class CategoryResource(UltraBlogResource):
    class Meta:
        queryset = Category.objects.all()

