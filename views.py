# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Behnam AhmadKhanBeigi ( b3hnam@gnu.org )
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
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404

from models.base import Category
from models import Post, Setting
from base import post_types


def blog_index(request):
    """
    Render the lastest blog entries.
    """
    ppp = Setting.get_setting("post_per_page")
    post_list = Post.objects.all()

    paginator = Paginator(post_list, ppp)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        postss = paginator.page(paginator.num_pages)

    return rr('ublog/index.html',
              {"posts": posts,
               "types": post_types.get_types_complex(),
               "rssfeed": "/blog/feed/"},
              context_instance=RequestContext(request))


def view_post(request, slug):
    """
    View a single post.
    """
    post = get_object_or_404(Post, slug=slug)

    return rr("ublog/view_post.html",
              {"post": post},
              context_instance=RequestContext(request))


def filter(request):
    """
    View posts filter by type or category
    """
    query = {}
    cat = request.GET.get('category', None)
    type_ = request.GET.get('type', None)
    if cat: query["categories__title__in"] = cat.split(",")
    if type_: query["post_type_name__in"] = type_.split(",")
    types = post_types.get_all_admin_forms()
    cats = Category.objects.all()
    posts = Post.objects.filter(**query)
    return rr("ublog/filter.html",
              {"posts": posts, "types":types, "cats":cats},
              context_instance=RequestContext(request))


def view_tag(request, tag):
    """
    Render the lastest blog entries with specifc tag.
    """
    from tagging.models import Tag, TaggedItem

    ppp = Setting.get_setting("post_per_page")
    try:
        tagobj = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        raise Http404()

    post_list = TaggedItem.objects.get_by_model(Post, tagobj)
    paginator = Paginator(post_list, ppp)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        postss = paginator.page(paginator.num_pages)

    return rr('ublog/index.html',
              {"posts": posts,
               "types": post_types.get_types_complex(),
               "rssfeed": "/blog/feed/"},
              context_instance=RequestContext(request))


def view_category(request, category):
    """
    Render the lastest blog entries in specific category.
    """
    ppp = Setting.get_setting("post_per_page")
    try:
        cat = Category.objects.get(slug=category)
    except Category.DoesNotExist:
        raise Http404()

    post_list = cat.ultra_blog_posts.all()
    paginator = Paginator(post_list, ppp)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        postss = paginator.page(paginator.num_pages)

    return rr('ublog/index.html',
              {"posts": posts,
               "types": post_types.get_types_complex(),
               "rssfeed": "/blog/feed/category/%s/" % category},
              context_instance=RequestContext(request))


def view_type(request, type_):
    return HttpResponse("asd")
