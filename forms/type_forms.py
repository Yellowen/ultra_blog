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
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.comments.forms import CommentForm

from ultra_blog.models import Post, TextPost, ImagePost, VideoPost, Category
from ultra_blog.base import post_types


class TextTypeForm(forms.ModelForm):
    fieldset = (_("Text Post"), {"fields": ("content", )})

    class Meta:
        model = TextPost

    ## class Media:
    ##     js = ("%sjs/nicEdit.js" % settings.MEDIA_URL,
    ##           "%sjs/js_init.js" % settings.MEDIA_URL,)
    ##     css = {'all': ("%scss/nicss.css" % settings.MEDIA_URL, )}


class ImageTypeForm(forms.ModelForm):
    fieldset = (_("Image Post"), {"fields": (("image", "alt"), "klass",
                                             ("width", "height"),
                                             "description")})

    class Meta:
        model = ImagePost


class VideoTypeForm(forms.ModelForm):
    fieldset = (_("Video Post"), {"fields": (("url", "videofile"),
                                             "mimetype",
                                             ("width", "height"),
                                             "desc")})

    class Meta:
        model = VideoPost
