
# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Some Hackers In Town
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
# ----------------------------------------------------------------------------

from django import forms
from django.contrib import admin
from django.conf.urls.defaults import url, patterns
from django.utils.html import escape
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.utils.encoding import force_unicode
from django.contrib.admin.options import csrf_protect_m
from django.db import models, transaction
from django.utils.functional import curry
from django.forms.models import modelform_factory
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.admin.util import (unquote, flatten_fieldsets,
                                       get_deleted_objects, model_format_dict)

from models import Category, Post, Blog, InvitationCode, BlogAlias
from base import post_types


class CategoryAdmin(admin.ModelAdmin):
    """
    Category model admin.
    """
    list_display = ("title", "slug", "parent")
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    """
    Post admin interface.
    """
    list_display = ("title", "author", "comments_count", "tags", "datetime",
                    "update_datetime", "publish", "post_type")

    list_filter = ("categories", )
    filter_horizontal   = ("categories", )
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class MicroAdmin(admin.ModelAdmin):
    """
    MicroPost admin interface.
    """
    list_display = ("content", "author", "status", "datetime", "site")

    list_filter = ("author", "status")
    search_fields = ["content", ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "founder", "active", "template", "aliases")


class AliasAdmin(admin.ModelAdmin):
    list_display = ("domain", "blog")


class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "date", "active", "blog")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogAlias, AliasAdmin)
admin.site.register(InvitationCode, InvitationCodeAdmin)
