.. _configuration:

.. image:: _static/images/logo.svg
   :width: 100px
   :alt: elastalk
   :align: right

.. toctree::
    :glob:


Configuring Your Connection
===========================

Configuration from Objects
--------------------------

If you're wanting to configure your connection from a python object, you're likely using
:ref:`Flask <elastalk_and_flask>`.  There is another article on that subject called
:ref:`elastalk_flask_config_from_objects`.

Configuration from TOML
-----------------------

In addition to :ref:`configuring from objects <elastalk_flask_config_from_objects>`, you can also
configure `elastalk` connections using `TOML <https://pypi.org/project/toml/>`_.

    TOML aims to be a minimal configuration file format that's easy to read due to obvious
    semantics.  TOML is designed to map unambiguously to a
    `hash table <https://en.wikipedia.org/wiki/Hash_table>`_.

    -- the TOML project's `README.md <https://github.com/toml-lang/toml>`_

.. _example_toml_configuration:

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

    :seeds: a list, or comma-separated string containing the Elasticsearch
        `seed hosts <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery-zen.html>`_

        .. seealso::

            :py:attr:`Elastalk.seeds <elastalk.config.ElastalkConf.sniff_on_start>`

    :sniff_on_start:  See
        `Sniffing on startup <https://www.elastic.co/guide/en/elasticsearch/client/net-api/current/sniffing-on-startup.html>`_
        and :py:attr:`ElastalkConf.sniff_on_start <elastalk.config.ElastalkConf.sniff_on_start>`

    :sniff_on_connection_fail:  See
        `Sniffing on connection failure <https://www.elastic.co/guide/en/elasticsearch/client/net-api/current/sniffing-on-connection-failure.html>`_
        and :py:attr:`ElastalkConf.sniff_on_connection_fail <elastalk.config.ElastalkConf.sniff_on_connection_fail>`

    :sniffer_timeout: See
        `Python Elasticsearch Client <https://elasticsearch-py.readthedocs.io/en/master/index.html?highlight=sniffer_timeout>`_
        and :py:attr:`ElastalkConf.sniffer_timeout <elastalk.config.ElastalkConf.sniffer_timeout>`

    :maxsize: the maximum number of concurrent connections the client may make

        .. seealso::

            :py:attr:`Elastalk.maxsize <elastalk.config.ElastalkConf.maxsize>`

    :mapping_field_limit: the maximum number of fields in an index

        .. note::

            Field and object mappings, as well as field aliases count towards this limit.

        .. seealso::

            * :py:attr:`ElastalkConf.mapping_field_limit <elastalk.config.ElastalkConf.mapping_field_limit>`
            * `Elasticsearch Mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping>`_

.. _configuration_blobs:

blobs
=====

This section contains global configuration options that control how, when, and which data is
converted to binary representations (see :ref:`Blobbing <blobbing>`).

    :enabled: indicates whether or not blobbing is enabled

    :excluded: the names of attributes that are never included in binary representations when a
        document is packed using the
        :py:func:`ElastalkConnection.pack() <elastalk.connect.ElastalkConnection.pack>`
        method

    :key: the key that stores blobbed values in packed documents

indexes
=======

This section contains information about specific
`Elasticsearch Indexes <https://www.elastic.co/blog/what-is-an-elasticsearch-index>`_.  In the
:ref:`example <example_toml_configuration>` above there are two configured indexes: `cats` and
`dogs`.  You can configure individual index preferences by adding creating a new section and
appending the index name to `indexes`.

    :blobs: index-level blob configuration (See :ref:`configuration_blobs`.)

    :mappings: a path to a file that contains an index mapping definition
        (See :ref:`seed_data_mappings`.)
