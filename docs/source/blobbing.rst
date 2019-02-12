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

Within the `blobs` key you can supply two directives:

    :enabled: *(bool)* `true` to convert seed data to BLOBs

    :exclude: *(list)* a list of top-level keys in your seed data document that should not be
        included in the BLOB

TODO: Convert to TOML.

.. code-block:: javascript

    {
      "blobs": {
        "enabled": true,
        "exclude": [
          "firstName",
          "lastName"
        ]
      }
    }
