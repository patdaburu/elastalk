.. _elastalk_and_flask:

.. image:: _static/images/logo.svg
   :width: 100px
   :alt: elastalk
   :align: right

.. toctree::
    :glob:

**********************
`elastalk` and `Flask`
**********************

When we built this library we figured you just might want to use it in your
`Flask <http://flask.pocoo.org/>`_ applications.  With that in mind we've provided a
few conveniences.

.. _elastalk_flask_config_from_objects:

Configuration from Objects
--------------------------

Flask applications objects support a convention that allows you to configure the application
using the name of a `Python class <https://docs.python.org/3/tutorial/classes.html>`_ via a method
on the application's configuration object called
`from_object() <http://flask.pocoo.org/docs/1.0/config/#configuring-from-files>`_.

Sticking with that convention, the
:py:class:`ElastalkConnection <elastalk.connect.ElastalkConnection>` in this
library has :py:attr:`config <elastalk.connect.ElastalkConnection.config>` attribute
which returns an :py:class:`ElastalkConf <elastalk.config.ElastalkConf>`.
Like the Flask configuration object, this configuration object supports a method called
:py:func:`from_object <elastalk.config.ElastalkConf.from_object>` that mirrors the
behavior of the Flask method.

Options
^^^^^^^

This section describes the configuration options you can use when configuring your Elasticsearch
settings from an object.

:ESHOSTS: a Python list, or comma-separated string containing the Elasticsearch
    `seed hosts <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery-zen.html>`_

    .. seealso::

        :py:attr:`ElasticsearchConf.seeds <elastalk.config.ElastalkConf.sniff_on_start>`

:ES_SNIFF_ON_START:  See
    `Sniffing on startup <https://www.elastic.co/guide/en/elasticsearch/client/net-api/current/sniffing-on-startup.html>`_
    and :py:attr:`ElastalkConf.sniff_on_start <elastalk.config.ElastalkConf.sniff_on_start>`

:ES_SNIFF_ON_CONNECTION_FAIL:  See
    `Sniffing on connection failure <https://www.elastic.co/guide/en/elasticsearch/client/net-api/current/sniffing-on-connection-failure.html>`_
    and :py:attr:`ElastalkConf.sniff_on_connection_fail <elastalk.config.ElastalkConf.sniff_on_connection_fail>`

:ES_SNIFFER_TIMEOUT: See
    `Python Elasticsearch Client <https://elasticsearch-py.readthedocs.io/en/master/index.html?highlight=sniffer_timeout>`_
    and :py:attr:`ElastalkConf.sniffer_timeout <elastalk.config.ElastalkConf.sniffer_timeout>`

:ES_MAXSIZE: the maximum number of concurrent connections the client may make

    .. seealso::

        :py:attr:`ElasticsearchConf.maxsize <elastalk.config.ElastalkConf.maxsize>`

:ES_MAPPING_FIELD_LIMIT: the maximum number of fields in an index

    .. note::

        Field and object mappings, as well as field aliases count towards this limit.

    .. seealso::

        * :py:attr:`ElastalkConf.mapping_field_limit <elastalk.config.ElastalkConf.mapping_field_limit>`
        * `Elasticsearch Mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping>`_



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
converted to binary representations (*"BLOBS"*).

    :excluded: the names of attributes that are never included in binary representations when a
        document is packed using the
        :py:func:`ElastalkConnection.pack() <elastalk.connect.ElastalkConnection.pack>`
        method

TODO

indexes
=======

TODO


