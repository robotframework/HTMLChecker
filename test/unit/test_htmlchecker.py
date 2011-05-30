import os
from nose.tools import *

from HTMLChecker import HTMLChecker

def test_soup_is_cached_when_same_file_is_used_by_subsequent_keywords():
    lib = HTMLChecker()
    valid_html_file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'valid.html')
    ok_(lib._soup_from_file(valid_html_file) is lib._soup_from_file(valid_html_file) )
    
