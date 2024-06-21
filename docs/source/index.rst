.. sphinxcontrib-d2 documentation master file, created by
   sphinx-quickstart on Fri Jun 21 09:02:56 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

d2-lang Sphinx Extension
========================

This is the documentation for the `d2-lang` Sphinx extension, which is a extension that allows you to write `d2 code <https://d2lang.com/>`_ in your Sphinx documentation.

Note this project is not affiliated with the `d2-lang` project. I just enjoy using it and wanted to make it easier to use in my documentation.

Installation
------------

To install the extension, you can use pip:

.. code-block:: bash

    pip install sphinxcontrib-d2

You must also install d2 itself. Follow the instructions in the `d2 documentation <https://d2lang.com/tour/install>`_.


Usage
-----

To use the extension, add it to the `extensions` list in your `conf.py`:

.. code-block:: python

    extensions = [
        'sphinxcontrib.d2',
    ]

Then, you can write D2 code in your documentation like this:

.. code-block::

      .. d2::
   
         x -> y


Configuration in `conf.py`
--------------------------

The extension has a few configuration options that you can set in your `conf.py`. All of these options must be put into a dictionary called `d2_config`:

- `d2_path`: The path to the d2-lang executable. By default, it is assumed to be in your PATH.
- `d2_flags`: A list of flags to pass to the d2-lang executable. By default, this is an empty list.
- `format`: The format to use when rendering the output images. By default, this is `svg`. Other options are `png` and `pdf`.


Here is an example of how you might set these options in your `conf.py`:

.. code-block:: python

    d2_config = {
        'd2_path': '/path/to/d2-lang',
        'd2_flags': ['--flag1', '--flag2 arg'],
        'format': 'svg',
    }


Configure in directive
----------------------

You can also configure the extension on a per-directive basis by passing options to the directive. The options are:

- `alt` (str): The alt text for the image.
- `caption` (str): The caption for the image.

Here is an example of how you might use these options:

.. code-block::

      .. d2::
         :alt: A d2 diagram
         :caption: This is a d2 diagram

         x -> y



Examples
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   example.rst
   example_myst.md



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
