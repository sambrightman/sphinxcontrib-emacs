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
Test utilities for Lisp processing.
"""

import sexpdata
import pytest

import sphinxcontrib.emacs.lisp.util as lisp_util


#: A little shortcut to parse lisp expression
l = sexpdata.loads


@pytest.mark.parametrize('sexp,is_quoted', [
    (l('"spam"'), False),
    (l('spam'), False),
    (l('(spam)'), False),
    (l("'(spam)"), True),
    (l("'spam"), True),
])
def test_is_quoted(sexp, is_quoted):
    assert lisp_util.is_quoted(sexp) == is_quoted


@pytest.mark.parametrize('sexp,is_quoted', [
    (l('"spam"'), False),
    (l('spam'), False),
    (l('(spam)'), False),
    (l("'(spam)"), False),
    (l("'spam"), True)
])
def test_is_quoted_symbol(sexp, is_quoted):
    assert lisp_util.is_quoted_symbol(sexp) == is_quoted


@pytest.mark.parametrize('sexp,is_primitive', [
    (l('1'), True),
    (l('()'), True),
    (l('nil'), True),
    (l('"spam"'), True),
    (l('t'), True),
    (l('(spam eggs)'), False),
    (l("'spam"), False)
])
def test_is_primitive(sexp, is_primitive):
    assert lisp_util.is_primitive(sexp) == is_primitive


@pytest.mark.parametrize('sexp,unquoted_sexp', [
    (l("'spam"), l('spam')),
    (l("'(spam eggs)"), l('(spam eggs)')),
])
def test_unquote(sexp, unquoted_sexp):
    assert lisp_util.unquote(sexp) == unquoted_sexp


@pytest.mark.parametrize('sexp', [
    l('spam'),
    l('(spam eggs)'),
    l('"spam"'),
    l('1'),
    l('t'),
    l('()'),
])
def test_unquote_not_quoted(sexp):
    with pytest.raises(ValueError) as excinfo:
        lisp_util.unquote(sexp)
    assert str(excinfo.value) == 'Not a quoted expression: {0!r}'.format(sexp)


@pytest.mark.parametrize('sexp,car,cdr', [
    (l('(spam . eggs)'), l('spam'), l('eggs')),
    (l('(spam . (with eggs))'), l('spam'), l('(with eggs)')),
    (l('("spam" . 1)'), 'spam', 1),
])
def test_parse_cons_cell(sexp, car, cdr):
    assert lisp_util.parse_cons_cell(sexp) == (car, cdr)


@pytest.mark.parametrize('sexp', [
    l('spam'),
    l('(spam eggs)'),
    l('(spam with eggs)'),
    l('"eggs"'),
    l('1'),
    l('t'),
    l('()'),
])
def test_parse_cons_cell_no_cons_cell(sexp):
    with pytest.raises(ValueError) as excinfo:
        lisp_util.parse_cons_cell(sexp)
    assert str(excinfo.value) == 'Not a cons cell: {0!r}'.format(sexp)


def test_parse_plist():
    plist = l('(:spam \'eggs :hello "world" :no 1)')
    assert lisp_util.parse_plist(plist) == {
        ':spam': l("'eggs"),
        ':hello': 'world',
        ':no': 1
    }

def test_parse_plist_no_list():
    with pytest.raises(ValueError) as excinfo:
        lisp_util.parse_plist(1)
    assert str(excinfo.value) == 'Not a list: 1'


def parse_package_version_quoted():
    assert lisp_util.parse_package_version(l('\'(spam . "1")')) == ('spam', '1')


def parse_package_version_unquoted():
    assert lisp_util.parse_package_version(l('(spam . "1")')) == ('spam', '1')


@pytest.mark.parametrize('sexp', [
    '("spam" . "1")',
    '(spam . 1)',
    '(spam . with-eggs)'
])
def parse_package_version_invalid(sexp):
    with pytest.raises(ValueError) as excinfo:
        lisp_util.parse_package_version(sexp)
    assert str(excinfo.value) == \
        'Not a valid :package-version: {0!r}'.format(sexp)
