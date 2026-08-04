# pytidal

3 Tidal catalog bulk harvesters grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `tidal_albums` | `tidal_albums` | Sequential Tidal album ID scan (OG tags) |
| `tidal_tracks` | `tidal_tracks` | Sequential Tidal track ID scan (OG tags) |
| `tidal_artists` | `tidal_artists` | Sequential Tidal artist ID scan (OG tags) |

## Install

```bash
pip install pytidal
# or, for the HuggingFace publisher (via harvestkit):
pip install "pytidal[hf]"
# or, for Cloudflare-guarded sources:
pip install "pytidal[stealth]"
```

## Usage

```bash
# list every registered scraper
pytidal-harvest --list

# harvest one source (resumable — safe to Ctrl-C and rerun)
pytidal-harvest tidal_albums --output ~/.cache/metadatarr/scrapers/ --start 1 --end 10000000
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
