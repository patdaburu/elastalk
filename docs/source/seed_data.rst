.. _seed_data:

.. image:: _static/images/logo.svg
   :width: 100px
   :alt: elastalk
   :align: right

.. toctree::
    :glob:

*****************************
Seeding Elasticsearch Indexes
*****************************

The :py:mod:`connect <elastalk.connect>` module contains a convenience function called
:py:func:`seed <elastalk.seed.seed>` that you can use to initialize
`Elasticsearch <https://www.elastic.co/products/elasticsearch>`_ indexes.

Directory Structure
*******************

When you call the :py:func:`seed <elastalk.seed.seed>` function you only need to provide a
path to the directory that contains your seed data, however the directory must conform to
particular structure.

And example seed data directory structure in the project is shown below.

.. code-block:: bash

    seed
    |-- config.toml
    `-- indexes
        |-- cats
        |   |-- cat
        |   |   |-- 5836327c-3592-4fcb-a925-14a106bdcdab
        |   |   `-- 9b31890a-28a1-4f59-a448-1f85dd2435a3
        |   `-- mappings.json
        `-- dogs
            `-- dog
                |-- 564e74ba-1177-4d3c-9160-a08e116ad9ff
                `-- de0a76e7-ecb9-4fac-b524-622ed8c344b8


The Base Directory (*"seed"*)
-----------------------------

This is the base directory that contains all the seed data.  If you're creating your own seed data
set you may provide another name.

.. _seed_data_indexes:

Indexes
-------

All of the `Elasticsearch indexes <https://www.elastic.co/blog/what-is-an-elasticsearch-index>`_
are defined in a subdirectory called *indexes*.  An Elasticsearch index will be created for each
subdirectory and the name of the subdirectory will be the name of the index.

.. _seed_data_document_types:

Document Types
--------------

Within each :ref:`index <seed_data_indexes>` directory there are directories that define
`document types <https://www.elastic.co/guide/en/elasticsearch/guide/current/mapping.html>`_.  The
name of the subdirectory will be the name of the document type.

.. _seed_data_documents:

Documents
---------

Within each :ref:`document type <seed_data_document_types>` directory are individual files that
represent the individual documents that will be indexed.  The name of the file will be the
`id <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html>`_ of
the document.

.. _seed_data_special_fields:

Special Fields
--------------

By convention, API seed data documents will often specify an `owner_` field and a `group_` field.
In both cases the value should be a string representation of a
`UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_.  These are not part
of the actual document but are used by applications to track stored documents.

If your data doesn't need these values, just omit one or both of them.

.. code-block:: python
    :linenos:
    :emphasize-lines: 2,3

    {
      "owner_": "3ab2b4e5-6992-43f0-851e-d1f42262cd55",
      "group_": "5bc9ad2d-7f72-452c-b32a-d699b20d2b1f",
      "timestamp_utc": "2018-12-10 16:36:05",
      "location": "/input/directory/data/in/arch/data.zip",
      "stats": {
        "name": "data.zip",
        "created_utc": "2018-10-12 10:56:39",
        "modified_utc": "2018-10-12 10:49:27",
        "size": 150044002
      },
      "metadata": {},
      "data_sources": [...]
    }


.. _seed_data_extra_config:

Extra Configuration
-------------------

You can supply additional information about the seed data in an index by supplying a `config.json`
file in the :ref:`seed_data_indexes` directory.

.. note::

    The :py:func:`seed <elastalk.seed.seed>` function supports a parameter called
    `config_filename` if, for some reason, you have a reason not to call your configuration files
    `"config.json"`.


.. _seed_data_mappings:

Mappings
^^^^^^^^

If your index has a static
`mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html>`_
you can include a `mappings` key in the
:ref:`index configuration file <seed_data_extra_config>`.  The value of this key should match what
you would provide in the `mappings` if you were creating the index directly.

For example, if you would create the index by submitting the following `PUT` request to
Elasticsearch...

.. code-block:: javascript

    PUT my_index
    {
      "mappings": {
        "_doc": {
          "properties": {
            "title":    { "type": "text"  },
            "name":     { "type": "text"  },
            "age":      { "type": "integer" },
            "created":  {
              "type":   "date",
              "format": "strict_date_optional_time||epoch_millis"
            }
          }
        }
      }
    }

...your configuration file should include a `mappings` key that looks like this...

.. code-block:: javascript

    {
      "mappings": {
        "_doc": {
          "properties": {
            "title": {
              "type": "text"
            },
            "name": {
              "type": "text"
            },
            "age": {
              "type": "integer"
            },
            "created": {
              "type": "date",
              "format": "strict_date_optional_time||epoch_millis"
            }
          }
        }
      }
    }

"Blobbing"
^^^^^^^^^^

In order to minimize database overhead, some applications may want to store non-searchable document
content in binary form in a field called `blob` so once a document has been indexed, if you inspect
it within the index (for example, using `Kibana <https://www.elastic.co/products/kibana>`_) you may
notice that the only visible fields are the :ref:`special fields <seed_data_special_fields>`.

If you want to store some (or all) of your seed data as a single
`base-64 <https://www.base64decode.org/>`_ `BLOB <https://techterms.com/definition/blob>`_, you can
add a `blobs` key to your :ref:`index configuration file <seed_data_extra_config>`.

Within the `blobs` key you can supply two directives:

    :enabled: *(bool)* `true` to convert seed data to BLOBs

    :exclude: *(list)* a list of top-level keys in your seed data document that should not be
        included in the BLOB

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

.. note::

    :ref:`seed_data_special_fields` are always excluded from BLOBs.
