==============
 Installation
==============

There are various ways to install this extension.

If you are not familiar with Python, the global installation may be the easiest
approach.

However, generally a per-project installation with virtualenv_ is recommended.

Global installation
===================

This extension is available from Python's package repository PyPI, and can be
installed with Python's package manager ``pip``:

.. code-block:: console

   $ pip install sphinxcontrib-emacs

Per project
===========

To install this extension per project, use virtualenv_ to create an isolated
Python environment.  Run the following commands for your project's top-level
directory:

.. code-block:: console

   $ echo '/.venv/' >> .gitignore   # Adapt this line to your VCS
   $ virtualenv -p "$(which python2.7)" .venv
   New python executable in .venv/bin/python2.7
   Also creating executable in .venv/bin/python
   Installing setuptools, pip...done
   $ source .venv/bin/activate
   $ echo $VIRTUAL_ENV
   …/.venv
   $ pip install sphinxcontrib-emacs

Now you can activate this environment in any shell session with `source
.venv/bin/activate`, to work on your documentation.

If you have virtualenvwrapper_ installed, it's a bit simpler:

.. code-block:: console

   $ mkvirtualenv -p "$(which python2.7)" myproject
   Running virtualenv with interpreter /usr/bin/python2.7
   New python executable in myproject/bin/python
   Installing setuptools, pip...done.
   $ pip install sphinxcontrib-emacs

You can activate this environment with `workon myproject`.

Read the docs
=============

.. todo::  Document setup of ReadTheDocs

.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
