# -*- coding: utf-8 -*-

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.angular import angular
from js.html5shiv import html5shiv
from js.fineuploader import fineuploader
from js.jquery import jquery
from js.jquery_form import jquery_form
from js.jquery_tablednd import jquery_tablednd
from js.jqueryui import bootstrap as jqueryui_bootstrap_theme
from js.jqueryui_tagit import tagit as ui_tagit
from zope.deprecation.deprecation import deprecated


# This is needed until ``kotti.views.form.deferred_tag_it_widget`` is converted
# to a class with a ``requirements`` attribute (that would be auto_needed by
# ``js.deform[_bootstrap]``).
tagit = Group([ui_tagit, jqueryui_bootstrap_theme])

# Kotti's resources
lib_kotti = Library("kotti", "static")

# ``js.bootstrap`` is only upgraded irregularly, so we bundle it on our own.
bootstrap_css = Resource(
    lib_kotti,
    'css/bootstrap.css',
    minified='css/bootstrap.min.css')
bootstrap_js = Resource(
    lib_kotti,
    'js/bootstrap.js',
    minified='js/bootstrap.min.js',
    depends=[jquery, ])

kotti_js = Resource(  # BBB
    lib_kotti,
    "js/kotti.js",
    minified="js/kotti.min.js",
    bottom=True)
contents_view_js = Resource(
    lib_kotti,
    "js/contents.js",
    depends=[kotti_js, jquery_tablednd, ],
    minified="js/contents.min.js",
    bottom=True)
base_css = Resource(
    lib_kotti,
    "css/base.css",
    depends=[bootstrap_css],
    minified="css/base.min.css",
    dont_bundle=True)
edit_css = Resource(  # BBB
    lib_kotti,
    "css/edit.css",
    depends=[base_css],
    minified="css/edit.min.css")
view_css = Resource(  # BBB
    lib_kotti,
    "css/view.css",
    depends=[base_css],
    minified="css/view.min.css")

# Resources for content upload views
upload_js = Resource(
    lib_kotti,
    "js/upload.js",
    depends=[angular, fineuploader],
    minified="js/upload.min.js",
    bottom=True)
upload_css = Resource(
    lib_kotti,
    "css/upload.css",
    depends=[base_css],
    minified="css/upload.min.css")
upload = Group([upload_js, upload_css])


class NeededGroup(object):
    """A collection of fanstatic resources that supports
       dynamic appending of resources after initialization"""

    def __init__(self, resources=[]):

        if not isinstance(resources, list):
            raise ValueError(
                "resources must be a list of fanstatic.Resource "
                "and/or fanstatic.Group objects")

        self.resources = []

        for resource in resources:
            self.add(resource)

    def add(self, resource):
        """resource may be a:

            - :class:`fanstatic.Resource` object or
            - :class:`fanstatic.Group` object"""

        if isinstance(resource, self.__class__):
            self.resources = self.resources + resource.resources
        elif isinstance(resource, (Resource, Group)):
            self.resources.append(resource)
        else:
            raise ValueError(
                "resource must be a NeededGroup,"
                "fanstatic.Resource or fanstatic.Group object")

    def need(self):  # pragma: no cover
        # this is tested in fanstatic itself; we should add browser tests
        # for `view_needed` and `edit_needed` (see below)
        Group(self.resources).need()

view_needed_css = NeededGroup([
    base_css,
    ])
view_needed_js = NeededGroup([
    jquery,
    bootstrap_js,
    html5shiv,
    ])
view_needed = NeededGroup([
    view_needed_css,
    view_needed_js,
    ])

edit_needed_css = NeededGroup([
    base_css,
    jqueryui_bootstrap_theme,
    ])
edit_needed_js = NeededGroup([
    jquery,
    bootstrap_js,
    html5shiv,
    # kotti_js,
    jquery_form,
    # deform_bootstrap_js,
    ])
edit_needed = NeededGroup([
    edit_needed_css,
    edit_needed_js,
    ])


for name in ('kotti_js', 'view_css', 'edit_css'):
    deprecated(name,
               "{} is deprecated as of Kotti 1.0.0 and will be no longer "
               "available starting with Kotti 2.0.0.".format(name))
