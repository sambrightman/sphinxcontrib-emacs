# -*- coding: utf-8; -*-
# Copyright (c) 2014-2015 Sebastian Wiesner <swiesner@lunaryorn.com>

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


"""Generic utilities."""


import re


def make_target(scope, name):
    """Create a target from ``scope`` and ``name``.

    ``name`` is the name of the Emacs Lisp symbol to reference, and ``scope``
    is the scope in which to reference the symbol.  Both arguments are strings.

    Return the target name as string.

    """
    return 'el.{0}.{1}'.format(scope, name)


def normalize_space(s):
    """Normalize whitespace in the given string.

    Remove leading and trailing whitespace, and collapse all other whitespace
    to a single space.

    """
    return re.sub(r'\s+', ' ', s.strip())
