#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import mock
import uuid
import pytest
from elastalk.connect import (
    ElastalkConnection,
    ElastalkMixin
)
from elastalk.config import (
    BlobConf,
    IndexConf,
    ElastalkConf,
    ElastalkConfigException
)


@pytest.fixture(scope='module', name='es_config')
def es_config_fixture() -> ElastalkConf:
    """
    This fixture returns an `ElasticsearchConf` (configuration) object.

    :return: the configuration object
    """
    return ElastalkConf()


def test_config(es_config: ElastalkConf):
    """
    Arrange: Create a new `ElastalkConnection`.
    Act: Obtain the configuration object via the `config` property.
    Assert: The configuration object returned is the object passed to the
        constructor.

    :param es_config: the Elasticsearch configuration
    """
    es_cnx = ElastalkConnection(config=es_config)
    assert es_cnx.config is es_config


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_client(es_config: ElastalkConf):
    """
    Arrange: Create a new `ElastalkConnection`.
    Act: Obtain an Elasticsearch client using the `client` property.
    Assert: The expected object is returned.

    :param es_config: the elastalk configuration
    """
    es_cnx = ElastalkConnection(config=es_config)
    es = es_cnx.client
    assert isinstance(es, mock.MagicMock)


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_client_idempotent(es_config: ElastalkConf):
    """
    Arrange: Create a new `ElastalkConnection`.
    Act: Obtain an Elasticsearch client using the `client` property, then
        retrieve the client again.
    Assert: The same object is returned both times.

    :param es_config: the elastalk configuration
    """
    es_cnx = ElastalkConnection(config=es_config)
    es1 = es_cnx.client
    es2 = es_cnx.client
    assert es1 is es2


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_client_config_error():
    """
    Arrange: Create a new `ElastalkConnection` with a bad configuration
        object.
    Act: Obtain an Elasticsearch client using the `client` property.
    Assert: The call to the property raises an `ElastalkConfigException`.
    """
    es_cnx = ElastalkConnection(
        config=ElastalkConf(seeds=[])
    )
    with pytest.raises(ElastalkConfigException):
        _ = es_cnx.client


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_client_set_config():
    """
    Arrange: Create an `ElastalkConnection` and retrieve the
        Elasticsearch client.
    Act: Re-configure the connection using the `config` property setter.
    Assert: The configuration and Elasticsearch client objects have changed.
    """
    cfg1 = ElastalkConf(seeds=['127.0.0.1'])
    es_cnx = ElastalkConnection(config=cfg1)
    es1 = es_cnx.client
    cfg2 = ElastalkConf(seeds=['test.daburu.net'])
    es_cnx.config = cfg2
    es2 = es_cnx.client

    assert cfg2 is not cfg1
    assert es2 is not es1


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_reset(es_config: ElastalkConf):
    """
    Arrange: Create a new `ElastalkConnection`.
    Act: Obtain an Elasticsearch client using the `client` property, call the
        `reset` method then retrieve the client again.
    Assert: A new object is returned the second time.

    :param es_config: the elastalk configuration
    """
    es_cnx = ElastalkConnection(config=es_config)
    es1 = es_cnx.client
    es_cnx.reset()
    es2 = es_cnx.client
    assert es1 is not es2


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
@pytest.mark.parametrize(
    'blobs_global, blobs_index', [
        (True, None),
        (False, None),
        (True, False)
    ]
)
def test_client_pack_unpack(
        es_config: ElastalkConf,
        blobs_global: bool,
        blobs_index: bool
):
    # Create the configuration.
    es_cfg = ElastalkConf(
        blobs=BlobConf(enabled=blobs_global, excluded={'a'})
    )
    es_cfg.indexes['test'] = IndexConf(
        blobs=BlobConf(enabled=blobs_index, excluded={'b'})
    )
    # Create the connection.
    es_cnx = ElastalkConnection(config=es_cfg)
    # Define the original data.
    original = {
        'a': str(uuid.uuid4()),
        'b': str(uuid.uuid4()),
        'c': str(uuid.uuid4())
    }
    # Pack...
    packed = es_cnx.pack(doc=original, index='test')

    # Assert that the packed document looks like it has actually been packed.
    assert 'a' in packed, "The 'a' key should not be included in the blob."
    assert 'b' in packed, "The 'b' key should not be included in the blob."
    # If blobs are enabled for the index, the 'c' key should be part of the
    # blob.  Otherwise it should remain part of the original document.
    if es_cfg.blobs_enabled(index='test'):
        assert 'c' not in packed, "The 'c' key should be included in the blob."
    else:
        assert 'c' in packed, "The 'c' key should not be included in the blob."

    # ...then unpack.
    unpacked = es_cnx.unpack(packed, index='test')
    # Assert!
    assert unpacked == original, \
        'The unpacked document should match the packed document.'


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_es_mixin_getters():
    """
    Arrange/Act: Construct an `ElastalkMixin` and retrieve the values of
        the `es_cnx` and `ex` properties.
    Assert: The properties return expected values.
    """
    mixin = ElastalkMixin()
    assert isinstance(mixin.es, mock.MagicMock)
    assert isinstance(mixin.es_cnx, ElastalkConnection)


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_es_mixin_setters():
    """
    Arrange/Act: Construct an `ElastalkMixin` and retrieve the values of
        the `es_cnx` and `ex` properties.
    Assert: The properties return expected values.
    """
    mixin = ElastalkMixin()
    cnx = ElastalkConnection()
    mixin.es_cnx = cnx
    assert isinstance(mixin.es, mock.MagicMock)
    assert mixin.es_cnx is cnx
