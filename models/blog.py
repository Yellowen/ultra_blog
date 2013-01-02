# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site


class Blog (models.Model):
    """
    Blog model.
    """
    STYLES = [
        ("", "---"),
        ('monokai', 'Monokai'),
        ('manni', 'Manni'),
        ('perldoc', 'Perldoc'),
        ('borland', 'Borland'),
        ('colorful', 'Colorful'),
        ('default', 'Default'),
        ('murphy', 'Murphy'),
        ('vs', 'Vs'),
        ('trac', 'Trac'),
        ('tango', 'Tango'),
        ('fruity', 'Fruity'),
        ('autumn', 'Autumn'),
        ('bw', 'Bw'),
        ('emacs', 'Emacs'),
        ('vim', 'Vim'),
        ('pastie', 'Pastie'),
        ('friendly', 'Friendly'),
        ('native', 'Native'),
        ]

    ANTISPAM = [
        ["0", "TypePad"],
        ["1", "Akismet"],
        ]

    title = models.CharField(_("title"), max_length=128)

    founder = models.ForeignKey('auth.User', verbose_name=_("founder"),
                                related_name="founder")
    authors = models.ManyToManyField('auth.User',
                                     verbose_name=_("authors"), null=True,
                                     related_name="authors")

    active = models.BooleanField(_("Active"),
                                 default=True)

    post_per_page = models.IntegerField(default=10,
                            verbose_name=_("How many post per page?"))

    comment_per_page = models.IntegerField(default=10,
                            verbose_name=_("How many comment per page?"))

    highlight_style = models.CharField(_("Highlight style"),
                                       max_length=16,
                                       choices=STYLES,
                                       default="emacs",
                                       blank=True)

    antispam = models.CharField(_("Anti-Spam"),
                                max_length=1,
                                choices=ANTISPAM,
                                null=True,
                                blank=True)

    spam_apikey = models.CharField(_("Anti-Spam API key"),
                                   max_length=100,
                                   help_text=_("Akismet or Typepad API key"),
                                   null=True,
                                   blank=True)

    template = models.CharField(_("template"), default="lxsameer.com",
                                max_length="64")

    @property
    def aliases(self):
        """
        Return a list of current blog aliases
        """
        a = BlogAlias.objects.filter(blog=self)
        a = " | ".join([i.domain for i in a])
        return a

    def __unicode__(self):
        return "%s-%s" % (self.founder, self.title)

    class Meta:
        app_label = "ultra_blog"
        verbose_name_plural = _("Blogs")
        verbose_name = _('Blog')


class BlogAlias(models.Model):
    blog = models.ForeignKey(Blog, verbose_name=_("Blog"))
    domain = models.URLField(_("domain"), unique=True)

    def __unicode__(self):
        return "%s:%s" % (self.domain, self.blog)

    class Meta:
        app_label = "ultra_blog"
        verbose_name_plural = _("Aliases")
        verbose_name = _('Alis')


class InvitationCode(models.Model):
    code = models.CharField(_("invatation code"), max_length=40)
    date = models.DateTimeField(_("used date"), blank=True,
                                null=True)
    active = models.BooleanField(_("active"), default=True)
    blog = models.ForeignKey(Blog, verbose_name=_("Used for"),
                             blank=True,
                             null=True)

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        super(InvitationCode, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s:%s" % (self.code, self.active)

    class Meta:
        app_label = "ultra_blog"
        verbose_name_plural = _("invitation codes")
        verbose_name = _('invitation code')
    
