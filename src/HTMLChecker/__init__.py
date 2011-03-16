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

    def validate_images(self, path):
        """Validates all image links in the given HTML file.

        Validates all image links in the given file and reports all errors at
        the end."""
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

    def get_images(self):
        return [Image(img, self._basedir) for img in self._soup.findAll('img')]

    def content(self):
        return ' '.join(t for t in self._collapse_tag(self._soup.body) if t)

    def _collapse_tag(self, tag):
        for elem in tag.contents:
            if elem.string is not None:
                yield elem.string.strip().replace('\n', ' ')
                continue
            for inner in self._collapse_tag(elem):
                yield inner


class Images(object):

    def __init__(self, soup):
        self._images = soup.get_images()

    def validate(self):
        self._report_missing_images([img.source for img in self._images
                                     if not img.exists()])

    def _report_missing_images(self, missing):
        if missing:
            if len(missing) == 1:
                self._report_single_missing_image(missing)
            self._report_multiple_missing_images(missing)

    def _report_single_missing_image(self, missing):
        raise AssertionError("Image '%s' does not exist" % missing[0])

    def _report_multiple_missing_images(self, missing):
        raise AssertionError("Images %s do not exist"
                             % ", ".join("'%s'" % m for m in missing))


class Image(object):

    def __init__(self, img_tag, basedir):
        self.source = img_tag['src']
        self._path = os.path.join(basedir, self.source)

    def exists(self):
        return os.path.isfile(self._path)
