.. _configuration:

.. image:: _static/images/logo.svg
   :width: 100px
   :alt: elastalk
   :align: right

.. toctree::
    :glob:


Configuring Your Connection
===========================

Configuration from TOML
-----------------------

In addition to :ref:`configuring from objects <elastalk_flask_config_from_objects>`, you can also
configure `elastalk` connections using `TOML <https://pypi.org/project/toml/>`_.

    TOML aims to be a minimal configuration file format that's easy to read due to obvious
    semantics.  TOML is designed to map unambiguously to a
    `hash table <https://en.wikipedia.org/wiki/Hash_table>`_.

    -- the TOML project's `README.md <https://github.com/toml-lang/toml>`_

A Sample TOML Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ini

    [blobs]
    excluded = ["owner_", "group_"]

    [indexes.cats]
    mappings = "cats/mappings.json"

    [indexes.dogs.blobs]
    enabled = True
    excluded = ["name", "breed"]

Options
^^^^^^^

blobs
=====

This section contains global configuration options that control how, when, and which data is
converted to binary representations (see :ref:`Blobbing <blobbing>`).

    :excluded: the names of attributes that are never included in binary representations when a
        document is packed using the
        :py:func:`ElastalkConnection.pack() <elastalk.connect.ElastalkConnection.pack>`
        method

TODO

indexes
=======

TODO


Configuration from Objects
--------------------------

If you're wanting to configure your connection from a python object, you're likely using
:ref:`Flask <elastalk_and_flask>`.  There is another article on that subject called
:ref:`elastalk_flask_config_from_objects`.
