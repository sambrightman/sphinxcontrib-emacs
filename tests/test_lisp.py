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
Tests for Lisp.
"""

import pytest

from sphinxcontrib.emacs import lisp

l = pytest.l


@pytest.fixture
def env():
    return lisp.AbstractEnvironment()


@pytest.fixture
def interpreter(request):
    return lisp.AbstractInterpreter([], env=request.getfuncargvalue('env'))


def test_broken_function_quotes():
    sexp = l("('eggs #'eggsp 'spam #'spamp)")
    assert lisp.strip_broken_function_quotes(sexp) == \
        l("('eggs 'eggsp 'spam 'spamp)")


def test_source_empty():
    assert not lisp.Source(file='foo', feature=None).empty
    assert not lisp.Source(file=None, feature='foo').empty
    assert lisp.Source(file=None, feature=None).empty


class TestAbstractEnvironment(object):

    def test_intern(self, env):
        spam = env.intern('spam')
        assert spam
        assert spam.name == 'spam'
        assert spam is env.top_level['spam']

    def test_intern_symbol(self, env):
        spam = env.intern(l('spam'))
        assert spam
        assert spam.name == 'spam'
        assert spam is env.top_level['spam']

    def test_intern_does_not_overwrite(self, env):
        spam = env.intern('spam')
        assert spam
        spam_new = env.intern('spam')
        assert spam is spam_new
        assert env.top_level['spam'] is spam

    def test_intern_invalid_symbol_name(self, env):
        sexp = l('(spam with eggs)')
        with pytest.raises(ValueError) as excinfo:
            env.intern(sexp)
        assert str(excinfo.value) == "Invalid symbol name: {0!r}".format(sexp)

    def test_provide_without_filename(self, env):
        feature = env.provide('spam')
        assert env.features == {'spam': feature}
        assert env.features['spam'] is feature
        assert feature.name == 'spam'
        assert feature.filename is None
        assert feature.load_time == 0

    def test_provide_with_filename(self, tmpdir, env):
        filename = tmpdir.join('spam.el')
        filename.write('A test file')
        feature = env.provide('eggs', filename=str(filename))
        assert env.features == {'eggs': feature}
        assert env.features['eggs'] is feature
        assert feature.name == 'eggs'
        assert feature.filename == filename
        assert feature.load_time == filename.mtime()

    def test_is_provided(self, env):
        assert not env.is_provided('spam')
        assert not env.is_provided('eggs')
        feature = env.provide('spam')
        assert env.is_provided(feature)
        assert env.is_provided('spam')
        assert not env.is_provided('eggs')


@pytest.mark.parametrize('form', [
    'defun', 'defun*', 'cl-defun', 'defmacro', 'defmacro*', 'cl-defmacro'
])
def test_defun_with_docstring(interpreter, env, form):
    interpreter.evals("""\
    ({form} spam (eggs &optional no &rest args)
      "A pointless function to make EGGS."
      (message "Foo"))
    """.format(form=form), context=dict(load_file_name='spam.el',
                                        load_feature='spam'))
    assert 'spam' in env.top_level
    spam = env.top_level['spam']
    assert spam.scopes == {'function': lisp.Source(file='spam.el',
                                                   feature='spam')}
    assert spam.properties == {
        'function-arglist': ['eggs', '&optional', 'no', '&rest', 'args'],
        'function-documentation': 'A pointless function to make EGGS.'
    }


@pytest.mark.parametrize('form', [
    'defun',
    'defun*',
    'cl-defun',
    'defmacro',
    'defmacro*',
    'cl-defmacro',
])
def test_defun_without_docstring(interpreter, env, form):
    interpreter.evals("""\
    ({form} spam (eggs &optional no &rest args)
      (message "Foo"))
    """.format(form=form), context=dict(load_file_name='spam.el',
                                        load_feature='spam'))
    assert 'spam' in env.top_level
    spam = env.top_level['spam']
    assert spam.scopes == {'function': lisp.Source(file='spam.el',
                                                   feature='spam')}
    assert spam.properties == {
        'function-arglist': ['eggs', '&optional', 'no', '&rest', 'args'],
    }


def test_defvar(interpreter, env):
    interpreter.evals("""\
    (defvar spam 'eggs "A useless variable.")""", context=dict(
        load_file_name='hello.el',
        load_feature='spam'
    ))
    assert 'spam' in env.top_level
    assert 'eggs' not in env.top_level
    spam = env.top_level['spam']
    assert spam.scopes == {'variable': lisp.Source(file='hello.el',
                                                   feature='spam')}
    assert spam.properties == {'variable-documentation': 'A useless variable.'}


def test_defvar_no_docstring(interpreter, env):
    interpreter.evals("(defvar spam 'eggs)", context=dict(
        load_file_name='hello.el',
        load_feature='spam'
    ))
    assert 'spam' in env.top_level
    assert 'eggs' not in env.top_level
    spam = env.top_level['spam']
    assert spam.scopes == {'variable': lisp.Source(file='hello.el',
                                                   feature='spam')}
    assert not spam.properties


def test_defvar_custom_args_ignored(interpreter, env):
    interpreter.evals("""\
    (defvar spam 'eggs "Foo"
       :safe 'stringp)""", context=dict(
        load_file_name='hello.el',
        load_feature='spam'
    ))
    assert 'spam' in env.top_level
    assert 'eggs' not in env.top_level
    spam = env.top_level['spam']
    assert spam.scopes == {'variable': lisp.Source(file='hello.el',
                                                   feature='spam')}
    assert spam.properties == {'variable-documentation': 'Foo'}


def test_defvar_local(interpreter, env):
    interpreter.evals('(defvar-local eggs 10 "Hello.")')
    assert 'eggs' in env.top_level
    eggs = env.top_level['eggs']
    assert eggs.scopes == {'variable': lisp.Source(file=None, feature=None)}
    assert eggs.properties == {
        'variable-documentation': 'Hello.',
        'buffer-local': True
    }


def test_defcustom_without_docstring(interpreter, env):
    interpreter.evals("""\
    (defcustom spam nil
       :package-version '(spam . "0.1")
       :risky t)
""")
    assert 'spam' in env.top_level
    spam = env.top_level['spam']
    assert spam.scopes == {'variable': lisp.Source(file=None, feature=None)}
    assert spam.properties == {
        'risky-local-variable': True,
        'custom-package-version': ('spam', '0.1')
    }


def test_defcustom_without_docstring(interpreter, env):
    interpreter.evals("""\
    (defcustom eggs nil
       "How many eggs to serve?"
       :package-version '(spam . "0.1")
       :safe 'integerp)
""")
    assert 'eggs' in env.top_level
    eggs = env.top_level['eggs']
    assert eggs.scopes == {'variable': lisp.Source(file=None, feature=None)}
    assert eggs.properties == {
        'variable-documentation': 'How many eggs to serve?',
        'safe-local-variable': 'integerp',
        'custom-package-version': ('spam', '0.1')
    }


def test_defface(interpreter, env):
    interpreter.evals("""\
    (defface eggs '((t :inherit error))
      "The face for eggs."
      :package-version '(spam . "10"))""")
    assert 'eggs' in env.top_level
    eggs = env.top_level['eggs']
    assert eggs.scopes == {'face': lisp.Source(file=None, feature=None)}
    assert eggs.properties == {
        'face-documentation': 'The face for eggs.',
        'custom-package-version': ('spam', '10')
    }


@pytest.mark.parametrize('value', [
    '"foo"',
    '1',
    't',
    'nil',
    '()',
])
def test_put_primitive_values(interpreter, env, value):
    interpreter.evals("(put 'spam 'eggs {value})".format(value=value))
    assert 'spam' in env.top_level
    spam = env.top_level['spam']
    assert spam.properties == {'eggs': l(value)}
    assert not spam.scopes


def test_put_symbol_value(interpreter, env):
    interpreter.evals("(put 'spam 'eggs 'hot)")
    assert 'spam' in env.top_level
    assert 'hot' in env.top_level
    spam = env.top_level['spam']
    hot = env.top_level['hot']
    assert spam.properties == {'eggs': hot}
    # We should really refer to the *same* object
    assert spam.properties['eggs'] is hot
    assert not spam.scopes
    assert not hot.scopes


def test_put_symbol_not_quoted(interpreter, env):
    interpreter.evals("(put spam 'eggs 1)")
    assert not env.top_level


def test_put_property_not_a_quoted_symbol(interpreter, env):
    interpreter.evals("(put 'spam eggs 1)")
    assert not env.top_level


def test_put_not_a_primitive_value(interpreter, env):
    interpreter.evals("(put 'spam 'eggs (foo))")
    assert not env.top_level


def test_make_variable_buffer_local(interpreter, env):
    interpreter.evals("(make-variable-buffer-local 'spam)")
    assert 'spam' in env.top_level
    spam = env.top_level['spam']
    assert spam.properties == {'buffer-local': True}
    assert not spam.scopes


def test_make_variable_buffer_local_not_a_quoted_symbol(interpreter, env):
    interpreter.evals("(make-variable-buffer-local spam)")
    assert not env.top_level


@pytest.mark.parametrize('form', [
    'progn',
    'eval-when-compile',
    'eval-and-compile',
])
def test_eval_inner(interpreter, env, form):
    interpreter.evals("""\
    ({form} (put 'spam 'eggs 1))
    """.format(form=form))
    assert 'spam' in env.top_level
    assert env.top_level['spam'].properties == {'eggs': 1}
