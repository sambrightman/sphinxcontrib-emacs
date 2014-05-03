========================
 Documenting Emacs Lisp
========================

.. default-domain:: rst

This extension provides directives and roles to document and cross-reference
Emacs Lisp symbols.

The Emacs Lisp domain
=====================

These directives live in the ``el`` domain.  See :ref:`domains` in the
Sphinx documentation for more information on the concept of domains.

You can set this domain as default domain to use the directives and roles
without their ``el:`` prefix, either globally, or per file.

To change the default domain globally, set the configuration value
``primary_domain`` in your :file:`conf.py` accordingly:

.. code-block:: python

   primary_domain = 'el'

To change the default domain per file, use the directive :dir:`default-domain`:

.. code-block:: rst

   .. default-domain:: el

Common options
==============

All directives support some common options:

``:noindex:``
   Suppress the creation of an index entry.  See
   :ref:`documenting-interactive-commands` for an example of using this
   directive.

``:auto:``
   Insert the docstring extracted from the Emacs Lisp source code of this
   symbol.

   For function-like symbols, also use the extracted function signature.  For
   variables, also insert various various variable properties, such as whether
   the variable is safe as buffer local variable, whether it is automatically
   buffer local, etc.

   Generally, the output of this option closely mirrors the appearance of
   docstrings in Emacs' built-in Help Mode.

   See :doc:`autodoc` for more information about automatically extracting
   docstrings.

Scopes
======

.. todo:: Explain scoping of description directives

Documenting functions and macros
================================

.. directive:: .. el:function:: symbol [argument ...] [&optional optional ...] [&rest args]
               .. el:macro:: symbol [argument ...] [&optional optional ...] [&rest args]

   Document ``symbol`` as function or macro with the given arglist, for example:

   .. code-block:: rst

      .. el:function:: hello name &optional greeting

         Greet the user with the given ``name``.

         If ``greeting`` is given, use it as greeting, instead of the standard
         “Hello”.

   Use :role:`el:function` and :role:`el:macro` to cross-reference symbols
   described with these directives.

.. role:: el:function
          el:macro

   Add a reference to a function or macro.

.. _documenting-interactive-commands:

Documenting interactive commands
================================

.. todo:: Document ``el:command:``

Documenting variables, user options and hooks
=============================================

.. directive:: .. el:variable:: symbol
               .. el:option:: symbol
               .. el:hook:: symbol

   Document ``symbol`` as Emacs Lisp variable, for example:

   .. code-block:: rst

      .. el:variable:: foo
         :local:
         :safe: stringp

         This variable does nothing particularly useful.

   This documents ``foo`` as buffer-local variable which is safe as local
   variable when its value matches the predicate ``stringp``.

   The flag ``:local:`` denotes that the variable is automatically buffer-local.

   The option ``:safe:`` denotes that the variable is safe as local variable
   with the given predicate.

   .. warning::

      Currently, this extension does not support lambda forms as arguments for
      ``:safe:``.  The value must be a symbol name denoting the predicate
      function.

      .. todo:: Add support for lambda predicates.

   The flag ``:risky:`` denotes that the variable is risky to use as local
   variable.

   With ``el:option`` or ``el:hook``, document ``symbol`` as customizable user
   option or hook respectively.  This does not affect cross-referencing, but
   uses a different description text for ``symbol``.

   Use :role:`el:option`, :role:`el:variable`, or :role:`el:hook` to
   cross-reference symbols described with these directives.

.. role:: el:variable
          el:option
          el:hook

   Insert a reference to a variable, option or hook respectively.

Documenting faces
=================

.. directive:: .. el:face:: symbol

   Document ``symbol`` as a face, for example:

   .. code-block:: rst

      .. el:face:: foo

         The face for foos.

.. role:: el:face

   Insert a reference to a face.

Documenting CL structs
======================

.. todo::
