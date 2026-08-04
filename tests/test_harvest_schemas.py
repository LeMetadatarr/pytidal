"""Row-schema equivalence tests for the 3 Tidal scrapers.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch7.py, keeping only the tests for scrapers that live in
this package, re-pointed at pytidal.harvest.*. These lock the exact flat-row
shape each scraper emits (the contract the LeData datasets depend on)
against a realistic upstream (OpenGraph HTML) sample, so a future engine
change can't silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pytidal.harvest.tidal_albums import TidalAlbumsSource
from pytidal.harvest.tidal_artists import TidalArtistsSource
from pytidal.harvest.tidal_tracks import TidalTracksSource

_ALBUM_HTML = """
<html><head>
<meta property="og:title" content="Discovery" />
<meta property="og:description" content="Album by Daft Punk &amp; Friends" />
<meta property="og:image" content="https://resources.tidal.com/images/album.jpg" />
</head></html>
"""

_TRACK_HTML = """
<html><head>
<meta property="og:title" content="One More Time" />
<meta property="og:description" content="Song by Daft Punk" />
<meta property="og:image" content="https://resources.tidal.com/images/track.jpg" />
</head></html>
"""

_ARTIST_HTML = """
<html><head>
<meta property="og:title" content="Daft Punk" />
<meta property="og:description" content="Listen to Daft Punk on TIDAL" />
<meta property="og:image" content="https://resources.tidal.com/images/artist.jpg" />
</head></html>
"""

_GENERIC_HTML = """
<html><head>
<meta property="og:title" content="TIDAL" />
</head></html>
"""


class _FakeResp:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


class _FakeSession:
    def __init__(self, html_by_id):
        self._html_by_id = html_by_id

    def get(self, url, timeout=None, allow_redirects=None):
        for tidal_id, html in self._html_by_id.items():
            if url.endswith(f"/{tidal_id}"):
                return _FakeResp(html)
        return _FakeResp(_GENERIC_HTML)


def test_tidal_albums_map_row_schema():
    src = TidalAlbumsSource()
    src._session = _FakeSession({1: _ALBUM_HTML, 2: _GENERIC_HTML})
    src.throttle.wait = lambda: None

    row = src._fetch_album(1)
    assert row == {
        "tidal_id": 1,
        "title": "Discovery",
        "artist": "Daft Punk & Friends",
        "description": "Album by Daft Punk & Friends",
        "image_url": "https://resources.tidal.com/images/album.jpg",
        "url": "https://tidal.com/album/1",
    }
    assert set(row) == {"tidal_id", "title", "artist", "description",
                        "image_url", "url"}

    # generic/unmapped page is skipped
    assert src._fetch_album(2) is None


def test_tidal_tracks_map_row_schema():
    src = TidalTracksSource()
    src._session = _FakeSession({1: _TRACK_HTML, 2: _GENERIC_HTML})
    src.throttle.wait = lambda: None

    row = src._fetch_track(1)
    assert row == {
        "tidal_id": 1,
        "title": "One More Time",
        "artist": "Daft Punk",
        "description": "Song by Daft Punk",
        "image_url": "https://resources.tidal.com/images/track.jpg",
        "url": "https://tidal.com/track/1",
    }
    assert set(row) == {"tidal_id", "title", "artist", "description",
                        "image_url", "url"}

    assert src._fetch_track(2) is None


def test_tidal_artists_map_row_schema():
    src = TidalArtistsSource()
    src._session = _FakeSession({1: _ARTIST_HTML, 2: _GENERIC_HTML})
    src.throttle.wait = lambda: None

    row = src._fetch_artist(1)
    assert row == {
        "tidal_id": 1,
        "name": "Daft Punk",
        "description": "Listen to Daft Punk on TIDAL",
        "image_url": "https://resources.tidal.com/images/artist.jpg",
        "url": "https://tidal.com/artist/1",
    }
    assert set(row) == {"tidal_id", "name", "description", "image_url", "url"}

    assert src._fetch_artist(2) is None


def test_tidal_scrapers_registered():
    reg = all_sources()
    assert reg.get("tidal_albums") is TidalAlbumsSource
    assert reg.get("tidal_tracks") is TidalTracksSource
    assert reg.get("tidal_artists") is TidalArtistsSource


def test_tidal_start_end_flags_bound_the_scan(monkeypatch):
    import argparse

    src = TidalAlbumsSource()
    src.configure(argparse.Namespace(start=5, end=6))
    assert src.initial_cursor() == 5
    # never hit the network: stub the per-id fetch
    monkeypatch.setattr(TidalAlbumsSource, "_fetch_album",
                        lambda self, tid: {"tidal_id": tid}, raising=True)
    rows, nxt = src.fetch(5)
    # chunk capped at end+1 -> ids 5,6 only; then terminate
    assert [r["tidal_id"] for r in rows] == [5, 6]
    assert nxt is None


def test_tidal_fetch_terminates_past_end(monkeypatch):
    import argparse

    src = TidalArtistsSource()
    src.configure(argparse.Namespace(start=1, end=10))
    rows, nxt = src.fetch(11)
    assert rows == [] and nxt is None
