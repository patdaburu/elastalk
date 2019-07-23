.. _blobbing:

.. image:: _static/images/logo.svg
   :width: 100px
   :alt: elastalk
   :align: right

.. toctree::
    :glob:


"Blobbing"
==========

In order to minimize database overhead, some applications may want to store non-searchable document
content in binary form in a field called `blob` so once a document has been indexed.

If you want to store some (or all) of your seed data as a single
`base-64 <https://www.base64decode.org/>`_ `BLOB <https://techterms.com/definition/blob>`_, you can
add a `blobs` key to your :ref:`index configuration file <seed_data_extra_config>`.

You can :ref:`configure <configuration>` blobbing behavior in your
:py:class:`ElastalkConnection <elastalk.connect.ElastalkConnection>` via the
:py:class:`ElastalkConf <elastalk.config.ElastalkConf>`.
