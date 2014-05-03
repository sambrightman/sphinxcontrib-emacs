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

      .. el:variable:: python-check-command
         :local:
         :safe: stringp

         The shell command to use for checking the current buffer.

   This documents ``python-check-command`` as buffer-local variable which is
   safe as local variable when its value matches the predicate ``stringp``.

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

      .. el:face:: error

         The face for errors.

.. role:: el:face

   Insert a reference to a face.

Documenting CL structs
======================

.. directive:: .. el:cl-struct:: symbol

   Document ``symbol`` as Cl struct defined by :code:`cl-defstruct`:

   .. code-block:: cl

      (cl-defstruct (person
                     (:constructor person-new)
                     (:constructor person-with-name name))
        name mobile)

   .. code-block:: rst

      .. el:cl-struct:: person

         A person.

         .. el:cl-slot:: name

            The name of a person

         .. el:cl-slot:: mobile

            The mobile phone number

      .. el:defun:: person-new :name name :mobile mobile

         Create a new person with the given ``name`` and ``mobile`` phone
         number.

      .. el:defun:: person-with-name name

         Create a new person with the given ``name``.

   Document constructors as standard functions with :dir:`el:function`.  For
   slots, use the special :dir:`el:cl-slot` directive:

   .. directive:: .. el:cl-slot:: slot

      Documents ``slot`` as a slot of the current Cl struct.

      .. warning::

         Using this directive **outside** of a :dir:`el:cl-struct` block is an
         error.

      As Cl slots are functions in Emacs Lisp, this directive creates a function
      reference to the slot.  Hence, the ``name`` slot from the above example
      can be referenced either with :role:`el:slot` or with :role:`el:function`:

      .. code-block:: rst

         The slot :el:cl-slot:`~person name` holds the name of a person.

         To get the name, call :el:function:`person-name`.

      In this example, both references would point to the description of
      ``name`` as in the example above.  The difference is merely in
      presentation: While :role:`el:function` always shows the entire function
      name, role:`el:cl-slot` only shows the name of the slot, if the reference
      appears inside a :dir:`el:cl-struct` block, or if the role text starts
      with a tilde.

.. role:: el:cl-slot

   Reference a slot of a Cl structure.

   The text of the role has the form :samp:`{struct} {slot}` where ``struct`` is
   the name of the structure containing the given ``slot``.  Inside of a
   :dir:`el:cl-struct` block, ``struct`` may be omitted in which case it
   defaults to the current structure.

   When referencing a slot of the current structure inside a :dir:`el:cl-struct`
   block, the name of the struct is omitted in the output.  To explicitly omit
   the struct name, prefix the role text with ``~``, as in
   :code:`:el:cl-slot:`~person name``.