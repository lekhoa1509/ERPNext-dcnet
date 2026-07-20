# API Reference: changelog_feed.py

**Language**: Python

**Source**: `desk/doctype/changelog_feed/changelog_feed.py`

---

## Classes

### ChangelogFeed

**Inherits from**: Document



## Functions

### fetch_changelog_feed()

Fetches changelog feed items from source using `get_changelog_feed` hook and stores in the db

**Returns**: (none)



### get_changelog_feed_items()

Returns a list of latest 10 changelog feed items

**Returns**: (none)



### _app_title(app_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |

**Returns**: (none)



### get_feed(since)

'What's New' feed implementation for Frappe

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| since | None | - | - |

**Returns**: (none)


