#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 1/23/19 by Pat Blair
"""
.. currentmodule:: elastalk.seed
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Prepare your Elasticsearch store with seed data!
"""
from pathlib import Path
from .config import ElastalkConf


def seed(root: str or Path,
         config: str or Path = 'config.toml',
         force: bool = False,):
    """
    Populate an Elasticsearch instance with seed data.

    :param root: the root directory that contains the seed data
    :param config: the path to the configuration
    :param force: delete existing indexes and replace them with seed data
    :raises FileNotFoundError: if the path does not exist
    :raises NotADirectoryError: if the path is not a directory
    """
    # Determine the root path.
    _root: Path = Path(root).resolve() if isinstance(root, str) else root
    # Determine the index path.
    indexes: Path = _root / 'indexes'
    # Raise exceptions if we don't find what we need.
    for path in [_root, indexes]:
        if not path.exists():
            raise FileNotFoundError(f"{str(path)} does not exist.")
        if not path.is_dir():
            raise NotADirectoryError(f"{str(path)} is not a directory.")

    # Let's get the configuration.
    _config: Path = (
        config if isinstance(config, Path) else Path(config)
    ).resolve()
    etconf = ElastalkConf().from_toml(toml_=_config)

    # TODO: Pick it up here!

