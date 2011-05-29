#  Copyright 2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

from lib.BeautifulSoup import BeautifulSoup
from version import VERSION


class HTMLChecker(object):
    """A test library to check and valdiate contents of HTML files.

    Currently, it only operates on files on the filesystem.
    """
    ROBOT_LIBRARY_VERSION = VERSION

    def validate_links(self, path):
        """Validates all links in the given HTML file.

        Goes through all the links in the file and reports validation errors
        in the end.

        A link is valid if the target file (href) exists and the (optional)
        anchor is defined inisde the target file.
        """
        self._soup_from_file(path)
        Links(self._soup).validate()

    def validate_images(self, path):
        """Validates all image links in the given HTML file.

        Goes through all the images in the file and reports validation errors
        in the end.

        An image is valid if the image file (src) it is pointing to can be
        found.
        """
        self._soup_from_file(path)
        Images(self._soup).validate()

    def _soup_from_file(self, path):
        self._soup = Soup(path)

    def get_content(self, path):
        """Returns all the text content without markup from given HTML file.

        Goes through the whole body of the file and reads text inside all tags.

        For example, given HTML:

        <body>
        <p>text <b>bolded</b> and <span>inside span</span> and more.</p>
        </body>

        this keyword returns "text bolded and inside span and more."
        """
        self._soup_from_file(path)
        return self._soup.content()


class Soup(object):

    def __init__(self, path):
        self._basedir = os.path.abspath(os.path.dirname(path))
        self._soup = self._get_soup(path)

    def _get_soup(self, path):
        with open(path) as infile:
            return BeautifulSoup(infile.read())

    def get_links(self):
        return [Link(t, self._basedir)
                for t in self._soup.findAll('a', href=True)]

    def get_anchors(self):
        return [t for t in self._soup.findAll('a')]

    def get_images(self):
        return [Image(t, self._basedir) for t in self._soup.findAll('img')]

    def all_tags(self):
        return [t for t in self._soup.findAll()]

    def content(self):
        return ' '.join(t for t in self._collapse_tag(self._soup.body) if t)

    def _collapse_tag(self, tag):
        for elem in tag.contents:
            if elem.string is not None:
                yield elem.string.strip().replace('\n', ' ')
                continue
            for inner in self._collapse_tag(elem):
                yield inner


class _Elements(object):

    def validate(self):
        invalids = self._invalid_items()
        if invalids:
            self._report_validation_error(invalids)

    def _report_validation_error(self, invalids):
        raise AssertionError(self._create_validation_error(invalids))

    def _create_validation_error(self, invalids):
        if len(invalids) == 1:
            return self._single_item_validation_error(invalids[0])
        return self._multi_item_validation_error(invalids)

    def _single_item_validation_error(self, invalid):
        return "%s %s does not exist" % (self.elem_type, invalid)

    def _multi_item_validation_error(self, invalids):
        return "%ss %s do not exist" % \
                (self.elem_type, ", ".join(str(i) for i in invalids))


class Links(_Elements):
    elem_type = "Link target"

    def __init__(self, soup):
        self._links = soup.get_links()

    def _invalid_items(self):
        return [l for l in self._links if not l.exists()]


class Images(_Elements):
    elem_type = "Image"

    def __init__(self, soup):
        self._images = soup.get_images()

    def _invalid_items(self):
        return [img for img in self._images if not img.exists()]


class Image(object):

    def __init__(self, img_tag, basedir):
        self._source = img_tag['src']
        self._path = os.path.join(basedir, self._source)

    def __str__(self):
        return "'%s'" % self._source

    def exists(self):
        return os.path.isfile(self._path)


class Link(object):

    def __init__(self, a_tag, basedir):
        self._target, self._anchor = self._parse_tag(a_tag)
        self._path = os.path.join(basedir, self._target)

    def _parse_tag(self, tag):
        parts = tag['href'].split('#')
        if len(parts) == 1:
            return parts[0], None
        return parts[0], parts[1]

    def __str__(self):
        s = self._target
        if self._anchor:
            s += '#%s' % self._anchor
        return  "'%s'" % s

    def exists(self):
        return self._validate_target() and self._validate_anchor()

    def _validate_target(self):
        return os.path.isfile(self._path)

    def _validate_anchor(self):
        if not self._anchor:
            return True
        soup = Soup(self._path)
        return any(t for t in soup.get_anchors() if self._matches_anchor(t)) or \
                any(t for t in soup.all_tags() if self._matches_anchor(t))

    def _matches_anchor(self, tag):
        return self._anchor in [tag.get('name', None), tag.get('id', None)]
