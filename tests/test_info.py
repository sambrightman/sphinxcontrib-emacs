# -*- coding: utf-8; -*-
# Copyright (c) 2014 Sebastian Wiesner <lunaryorn@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Test info manual support
"""

import requests
import pytest

from sphinxcontrib.emacs.info import (HTMLXRefDB, HTMLXREF_URL,
                                      expand_node_name)


@pytest.mark.info
@pytest.mark.parametrize('node,filename,anchor', [
    ('Structures', 'Structures', 'Structures'),
    ('Library  Search', 'Library-Search', 'Library-Search'),
    ('Multi-file  Packages', 'Multi_002dfile-Packages', 'Multi_002dfile-Packages'),
    ('%-Constructs', '_0025_002dConstructs', 'g_t_0025_002dConstructs'),
    ('Top', 'index', 'Top')
])
def test_expand_node_name(node, filename, anchor):
    assert expand_node_name(node) == (filename, anchor)
    assert expand_node_name('Structures') == ('Structures', 'Structures')


@pytest.fixture(scope='module')
def htmlxref_string():
    return requests.get(HTMLXREF_URL).text


@pytest.fixture(scope='module')
def xrefdb(request):
    return HTMLXRefDB.parse(request.getfuncargvalue('htmlxref_string'))


@pytest.mark.info
class TestHTMLXRefDB(object):

    def test_parse_does_not_raise_exception(self, htmlxref_string):
        HTMLXRefDB.parse(htmlxref_string)

    @pytest.mark.parametrize('manual,node,url', [
        ('cl', 'Structures',
         'http://www.gnu.org/software/emacs/manual/html_node/cl/Structures.html#Structures'),
        ('elisp', 'Library Search',
         'http://www.gnu.org/software/emacs/manual/html_node/elisp/Library-Search.html#Library-Search'),
        ('elisp', 'Multi-file Packages',
         'http://www.gnu.org/software/emacs/manual/html_node/elisp/Multi_002dfile-Packages.html#Multi_002dfile-Packages'),
        ('elisp', '%-Constructs',
         'http://www.gnu.org/software/emacs/manual/html_node/elisp/_0025_002dConstructs.html#g_t_0025_002dConstructs'),
        ('elisp', 'Top',
         'http://www.gnu.org/software/emacs/manual/html_node/elisp/index.html#Top')
    ])
    def test_resolve(self, xrefdb, manual, node, url):
        assert xrefdb.resolve(manual, node) == url
