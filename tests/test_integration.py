import re

import markdown

from changelog_slugs import ChangelogSlugifier

CHANGELOG = """
# Changelog

## [Unreleased]
### Added
### Fixed

## [1.0.0] resolved reference link
### Added
### Removed
### Security

## [0.1.0] unresolved reference link
### Added
### Changed
### Deprecated

## 0.0.1 plain heading
### Added

[Unreleased]: # (dummy link)
[1.0.0]: # (dummy link)
"""

EXPECTED_SLUGS = [
    "changelog",
    "unreleased",
    "added",
    "fixed",
    "v1-0-0",
    "v1-0-0-added",
    "v1-0-0-removed",
    "v1-0-0-security",
    "v0-1-0",
    "v0-1-0-added",
    "v0-1-0-changed",
    "v0-1-0-deprecated",
    "v0-0-1",
    "v0-0-1-added",
]

ID_RE = re.compile(r'^<h[1-3] id="([^"]+)"')


def test_markdown_toc_integration():
    html = markdown.markdown(
        CHANGELOG,
        extensions=["toc"],
        extension_configs={"toc": {"slugify": ChangelogSlugifier()}},
    )

    for line, expected in zip(html.splitlines(), EXPECTED_SLUGS, strict=True):
        match = ID_RE.search(line)
        assert match is not None
        assert match.group(1) == expected
