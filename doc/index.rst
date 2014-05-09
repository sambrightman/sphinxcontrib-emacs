==================================================
 sphinxcontrib-emacs — Document Emacs with Sphinx
==================================================

sphinxcontrib-emacs is a Sphinx_ extension to document Emacs_ code.

.. _Sphinx: http://sphinx-doc.org
.. _Emacs: http://www.gnu.org/software/emacs/

Features
========

- Description directives for Emacs Lisp symbols
- Autodoc for Emacs Lisp code
- Better Texinfo integration to build online manuals for Emacs

Status
======

This extension is in alpha state currently.

.. ifconfig:: todo_include_todos

   While it generally works well, there are a number of issues and lacking
   features:

   .. todolist::

   If you know Python and Sphinx, please help us with fixing these.

User Guide
==========

.. toctree::
   :maxdepth: 2

   guide/intro
   guide/installation
   guide/quickstart
   guide/domain
   guide/autodoc

License
=======

.. include:: ../LICENSE
   :literal:
