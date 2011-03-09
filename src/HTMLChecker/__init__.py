import os
from lib.BeautifulSoup import BeautifulSoup


class HTMLChecker(object):

    def validate_images(self, path):
        """Validates all image links in the given HTML file.

        Fails on the first broken link."""
        self._soup_from_file(path)
        for img in self._soup.get_images():
            img.validate()

    def _soup_from_file(self, path):
        self._soup = Soup(path)


class Soup(object):

    def __init__(self, path):
        self._basedir = os.path.abspath(os.path.dirname(path))
        self._soup = self._get_soup(path)

    def _get_soup(self, path):
        with open(path) as infile:
            return BeautifulSoup(infile.read())

    def get_images(self):
        return [Image(img, self._basedir) for img in self._soup.findAll('img')]


class Image(object):

    def __init__(self, img_tag, basedir):
        self._src = img_tag['src']
        self._path = os.path.join(basedir, self._src)

    def validate(self):
        if not os.path.isfile(self._path):
            raise AssertionError("Image '%s' does not exist" % self._src)
