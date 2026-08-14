# Dataset

## What this repo produces

`pytidal` harvests public metadata from Tidal pages by sequentially scanning album, track, and artist IDs. It extracts Open Graph tags from `tidal.com/album/{id}`, `tidal.com/track/{id}`, and `tidal.com/artist/{id}` pages. No API key or account is required. The output is up to three JSONL files, one per entity type.

## Dataset format

### `tidal_albums`

One row per album. Each row is a JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `tidal_id` | integer | Tidal album identifier. |
| `title` | string | Album title. |
| `artist` | string or null | Artist name parsed from the description. |
| `description` | string | Raw Open Graph description. |
| `image_url` | string or null | Cover image URL. |
| `url` | string | Tidal album page URL. |

### `tidal_tracks`

One row per track. Each row is a JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `tidal_id` | integer | Tidal track identifier. |
| `title` | string | Track title. |
| `artist` | string or null | Artist name parsed from the description. |
| `description` | string | Raw Open Graph description. |
| `image_url` | string or null | Cover image URL. |
| `url` | string | Tidal track page URL. |

### `tidal_artists`

One row per artist. Each row is a JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `tidal_id` | integer | Tidal artist identifier. |
| `name` | string | Artist name. |
| `description` | string | Raw Open Graph description. |
| `image_url` | string or null | Artist image URL. |
| `url` | string | Tidal artist page URL. |

## How to generate it

Install the package and run the harvesters with a start and end ID:

```bash
pip install pytidal

pytidal-harvest tidal_albums \
  --output ~/.cache/metadatarr/scrapers/ \
  --start 1 --end 10000000

pytidal-harvest tidal_tracks \
  --output ~/.cache/metadatarr/scrapers/ \
  --start 1 --end 10000000

pytidal-harvest tidal_artists \
  --output ~/.cache/metadatarr/scrapers/ \
  --start 1 --end 10000000
```

The harvests are resumable. You can stop any harvester with Ctrl-C and rerun the same command to continue from the last checkpoint.

## Worth publishing on Hugging Face?

No. The data is derived from Tidal public pages. Redistribution may violate the Tidal terms of service. The dataset is suitable for local research and internal metadata enrichment, but not for public redistribution.

## ML tasks served

- Music information retrieval.
- Album, track, and artist linking.
- Cover art retrieval and multimodal metadata tasks.
- Music recommendation and catalog enrichment.
