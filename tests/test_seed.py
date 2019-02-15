#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from unittest import mock
import pytest
from elastalk.seed import seed


@pytest.fixture(scope='module', name='es_config')
def es_config_fixture() -> Path:
    """
    This fixture returns an `ElasticsearchConf` (configuration) object.

    :return: the configuration object
    """
    return Path(__file__).resolve().parent / 'configs' / '001' / 'config.toml'


@pytest.fixture(scope='module', name='seed_root')
def seed_root_fixture() -> Path:
    """
    This fixture returns a path to the seed data defined for tests.

    :return: the path to the seed data root directory
    """
    return Path(__file__).resolve().parent / 'data' / 'seed'


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_seed_success(es_config: str, seed_root: Path):
    """
    Arrange/Act: Call the `seed` function with good parameters.
    Assert: No errors are observed.

    :param es_config: the Elasticsearch config
    :param seed_root: the path to the seed data directory
    """
    # TODO: Add assertions.
    seed(config=es_config, root=seed_root, force=True)


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock()
)
def test_seed_bad_seed_path(es_config: str, seed_root: Path):
    """
    Arrange/Act: Call the `seed` function with unacceptable `root` parameter
        values
    Assert: The correct exceptions are raised.

    :param es_config: the Elasticsearch config
    :param seed_root: the path to the seed data directory
    """
    with pytest.raises(FileNotFoundError):
        seed(config=es_config, root=seed_root / 'does_not_exist', force=True)

    with pytest.raises(NotADirectoryError):
        seed(config=es_config, root=Path(__file__).resolve(), force=True)


@mock.patch(
    'elasticsearch.Elasticsearch',
    lambda *args, **kwargs: mock.MagicMock(
        indices=mock.MagicMock(
            **{'exists.return_value': True}
        )
    )
)
def test_seed_index_exists(es_config: str, seed_root: Path):
    """
    Arrange: Mock an environment such that seed indexes will appear to exist.
    Act:  Call the `seed` function with a `force` argument of `False`.
    Assert: No errors are observed.

    :param es_config: the Elasticsearch config
    :param seed_root: the path to the seed data directory
    """
    # TODO: Add assertions.
    seed(config=es_config, root=seed_root, force=False)
