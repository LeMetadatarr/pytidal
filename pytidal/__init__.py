"""pytidal — Tidal catalog bulk harvesters, grouped on harvestkit.

Importing this package imports :mod:`pytidal.harvest`, which in turn
imports every scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pytidal.version import __version__

import pytidal.harvest  # noqa: F401  (import for @register side effects)

__all__ = ["__version__"]
