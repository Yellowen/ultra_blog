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

from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from ultra_blog.models import InvitationCode
from captcha.fields import ReCaptchaField


class RegisterBlogForm(forms.Form):
    name = forms.CharField(max_length=64)
    lang = forms.ChoiceField(choices=settings.LANGUAGES)
    captcha = ReCaptchaField()
    code = forms.CharField(label=_("activation code"),
                           max_length=128)

    def is_valid(self, *args, **kwargs):
        if super(RegisterBlogForm, self).is_valid(*args, **kwargs):
            try:
                inv_code = InvitationCode.objects.get(
                    code=self.cleaned_data['code'])

                if inv_code.active:
                    self.cleaned_data["code"] = inv_code

                    sub_pattern = re.compile("^[a-z][a-z0-9\-]+$")                
                    if not sub_pattern.match(self.cleaned_data["name"].lower()):
                        self.errors["name"] = [
                            _("invalid subdomain name. Don't use invalid characters."),
                            ]
                        return False

                    return True

                else:
                    self.errors["code"] = [_("Initation code is been used already")]
                    return False

            except InvitationCode.DoesNotExist:
                self.errors["code"] = [_("Initation code is not valid")]
                return False
        else:
            return False
