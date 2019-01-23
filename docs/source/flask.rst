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

Configuration from Objects
--------------------------

Flask applications objects support a convention that allows you to configure the application
using the name of a `Python class <https://docs.python.org/3/tutorial/classes.html>`_ via a method
on the application's configuration object called
`from_object() <http://flask.pocoo.org/docs/1.0/config/#configuring-from-files>`_.

Sticking with that convention, the
:py:class:`ElasticsearchConnection <elastalk.client.ElasticsearchConnection>` in this
library has :py:attr:`config <elastalk.client.ElasticsearchConnection.config>` attribute
which returns an :py:class:`ElasticsearchConf <elastalk.config.ElasticsearchConf>`.
Like the Flask configuration object, this configuration object supports a method called
:py:func:`from_object <elastalk.config.ElasticsearchConf.from_object>` that mirrors the
behavior of the Flask method.

Configuration Options
---------------------

This section describes the configuration options you can use when configuring your Elasticsearch
settings from an object.

:ESHOSTS: a Python list, or comma-separated string containing the Elasticsearch
    `seed hosts <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery-zen.html>`_

    .. seealso::

        :py:attr:`ElasticsearchConf.seeds <elastalk.config.ElasticsearchConf.sniff_on_start>`

:ES_SNIFF_ON_START:  See
    `Sniffing on startup <https://www.elastic.co/guide/en/elasticsearch/client/net-api/current/sniffing-on-startup.html>`_
    and :py:attr:`ElasticsearchConf.sniff_on_start <elastalk.config.ElasticsearchConf.sniff_on_start>`

:ES_SNIFF_ON_CONNECTION_FAIL:  See
    `Sniffing on connection failure <https://www.elastic.co/guide/en/elasticsearch/client/net-api/current/sniffing-on-connection-failure.html>`_
    and :py:attr:`ElasticsearchConf.sniff_on_connection_fail <elastalk.config.ElasticsearchConf.sniff_on_connection_fail>`

:ES_SNIFFER_TIMEOUT: See
    `Python Elasticsearch Client <https://elasticsearch-py.readthedocs.io/en/master/index.html?highlight=sniffer_timeout>`_
    and :py:attr:`ElasticsearchConf.sniffer_timeout <elastalk.config.ElasticsearchConf.sniffer_timeout>`

:ES_MAXSIZE: the maximum number of concurrent connections the client may make

    .. seealso::

        :py:attr:`ElasticsearchConf.maxsize <elastalk.config.ElasticsearchConf.maxsize>`

:ES_MAPPING_FIELD_LIMIT: the maximum number of fields in an index

    .. note::

        Field and object mappings, as well as field aliases count towards this limit.

    .. seealso::

        * :py:attr:`ElasticsearchConf.mapping_field_limit <elastalk.config.ElasticsearchConf.mapping_field_limit>`
        * `Elasticsearch Mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping>`_





