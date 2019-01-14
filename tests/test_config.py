#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Tuple
import pytest
from unittest import mock
from elastalk.config import ElastalkConf, IndexConf, BlobConf


def get_config(set_: str, name: str = 'config.toml') -> Tuple[Path, str]:
    path: Path = Path(__file__).parent.resolve() / 'configs' / set_ / name
    return path, path.read_text()


def get_config_root(set_: str) -> Path:
    return Path(__file__).parent.resolve() / 'configs' / set_


def test_elastalk_conf_defaults():
    """
    Arrange/Act: Construct a new `ElasticsearchConf` with defaults.
    Assert: Property values match expectations.
    """
    # Arrange/Act: Create the object.
    esc = ElastalkConf()
    # Verify the properties.
    assert esc.seeds == ['127.0.0.1'], \
        'Default seed hosts should include only the local host.'
    assert esc.sniff_on_start is True, \
        'Sniffing on startup should be enabled by default.'
    assert esc.sniff_on_connection_fail is True, \
        'Sniffing when the connection fails should be enabled by default.'
    assert esc.sniffer_timeout == 60, \
        'The sniffer timeout should be 60 seconds by default.'
    assert esc.maxsize == 10, \
        'The maximum number of connections should be 10 by default.'
    assert esc.mapping_field_limit == 1000, \
        'The mapping field limit should be 1000 by default.'
    assert esc.blobs == BlobConf(), \
        'Blobbing configuration should be default.'
    assert esc.indexes == {}, \
        'Index configuration should be empty.'


def test_blob_conf_defaults():
    """
    Arrange/Act: Construct an instance of `BlobConf` with default values.
    Assert:  Default values match expected values.
    """
    bcfg = BlobConf()
    assert not bcfg.enabled, \
        'Blobbing should be disabled.'
    assert bcfg.excluded == set(), \
        'Exclusions should be an empty set.'
    assert bcfg.key is None, \
        'The blob key should be `None`.'


def test_index_conf_defaults():
    """
    Arrange/Act: Construct an instance of `IndexConf` with default values.
    Assert:  Default values match expected values.
    """
    idx_cfg = IndexConf()
    assert idx_cfg.blobs == BlobConf(), \
        'Blobbing configuration should be default.'
    assert idx_cfg.mappings is None, \
        'The `mappings` property should be `None`.'


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
@pytest.mark.parametrize(
    'blobs_global, blobs_index, blobs_final', [
        (True, None, True),
        (False, None, False),
        (True, False, False),
        (False, True, True)
    ]
)
def test_client_pack_unpack(
        blobs_global: bool,
        blobs_index: bool,
        blobs_final: bool
):
    # Create the configuration.
    es_cfg = ElastalkConf(
        blobs=BlobConf(enabled=blobs_global, excluded={'a'})
    )
    es_cfg.indexes['test'] = IndexConf(
        blobs=BlobConf(enabled=blobs_index, excluded={'b'})
    )
    # Assert that blobs are enabled (or disabled) for the index according to
    # expectations.
    assert es_cfg.blobs_enabled(index='test') == blobs_final, \
        "The blobs_enabled() method should return the `blobs_final` value."
    # Assert the blobs are enabled (or disabled) for unconfigured indexes
    # by the global value.
    assert es_cfg.blobs_enabled(index='not_configured') == blobs_global, \
        "The blobs_enabled() method should return the global value for " \
        "unconfigured indexes."


def test_config_from_toml_001():
    """
    Arrange:  Create an `ElastalkConf` instance.
    Act:  Configure the instance from configuration 001.
    Assert:  The configuration matches expectations.
    """
    config = ElastalkConf()

    for toml in get_config('001'):
        config.from_toml(toml_=toml)

        # Assert: global blobbing
        assert config.blobs.enabled is True, \
            'Blobbing should be enabled.'
        assert config.blobs.excluded == {"owner_", "group_"}, \
            'The list of global exclusions should match the expectations.'

        # Assert: index mappings for the 'cats' index
        assert config.indexes['cats'].mappings == "cats/mappings.json", \
            'The path to the mappings document should match the expectation.'
        # Validate the contents of the mappings document.
        mappings_doc = config.indexes['cats'].mappings_document(
            root=get_config_root('001')
        )
        assert 'mappings' in mappings_doc, \
            "The mappings document should contain the 'mappings' key."

        # Assert: blobbing for the 'cats' index
        assert not config.indexes['cats'].blobs.enabled, \
            "Blobbing should be disabled for the 'cats' index."
        assert config.indexes['cats'].blobs.excluded == set(), \
            "The list of exclusions for the 'cats' index should be empty."
        assert config.blobs_enabled(index='cats'), \
            "Blobbing for the 'cats' index should be enabled per the global " \
            "configuration."
        assert (
                config.blob_exclusions(index='cats') == config.blobs.excluded
        ), "Blobs exclusions for the 'cats' index should match the global " \
           "exclusions."

        # Assert: index mappings for the 'cats' index
        assert config.indexes['cats'].mappings == "cats/mappings.json", \
            'The path to the mappings document should match the expectation.'
        # Validate the contents of the mappings document.
        assert config.indexes['dogs'].mappings_document(
            root=get_config_root('001')) is None, \
            "Index mapping should not be configured for the 'dogs' index."

        # Assert: blobbing for the 'dogs' index
        assert config.indexes['dogs'].blobs.enabled is True, \
            "Blobbing should be enabled for the 'dogs' index."

        assert config.indexes['dogs'].blobs.excluded == {"name", "breed"}, \
            "The list of blob exclusions for the 'dogs' index should match " \
            "the expectations."

        assert config.blobs_enabled(index='dogs'), \
            "Blobbing for the 'dogs' index should be enabled."

        assert (
                config.blob_exclusions(index='dogs') ==
                config.blobs.excluded | config.indexes['dogs'].blobs.excluded
        ), "Blobs exclusions for the 'dogs' index should contain the global " \
           "exclusions and those configured for the index."

