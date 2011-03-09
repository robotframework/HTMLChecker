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

    def get_content(self, path):
        """Returns all the textual from given HTML file.

        Goes through the whole body of the file and reads text inside all tags.

        For example, given HTML:
            <body>
              <p>text <b>bolded</b> and <span>inside span</span> and more.</p>
            </body>
        this keyword returns "text bolded and inside spand and more."
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
                yield elem.string.strip()
                continue
            for inner in self._collapse_tag(elem):
                yield inner


class Image(object):

    def __init__(self, img_tag, basedir):
        self._src = img_tag['src']
        self._path = os.path.join(basedir, self._src)

    def validate(self):
        if not os.path.isfile(self._path):
            raise AssertionError("Image '%s' does not exist" % self._src)
