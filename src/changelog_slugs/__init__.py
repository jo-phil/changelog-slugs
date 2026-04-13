"""Changelog-aware heading slugs for Python-Markdown."""

__all__ = ["Slugifier", "slugify"]

import re

from markdown.extensions.toc import slugify as default_slugify

# Recommended SemVer regex, with start/end anchors removed for embedding.
# See https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
_VERSION_PATTERN = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"

# Pattern for strings that begin with a semantic version.
# - Allow a leading '[' from unresolved links.
# - Allow an optional 'v' prefix.
# - Avoid partial matches by disallowing trailing SemVer characters.
_RELEASE_PATTERN = re.compile(
    rf"^\[?v?(?P<version>{_VERSION_PATTERN})(?![0-9A-Za-z.+-])"
)

_CHANGE_GROUPS = {
    "added",
    "changed",
    "deprecated",
    "removed",
    "fixed",
    "security",
}


class Slugifier:
    """Slugifier for changelog headings with release-scoped change groups.

    It recognizes release headings that begin with a version following
    [SemVer](https://semver.org), optionally prefixed with `v`. For example,
    `[0.1.0] - 2026-04-11`, `0.1.0 some text`, and `v0.1.0` all resolve
    to the release slug `v0-1-0`.

    Subsequent headings that match standard Keep a Changelog change groups
    are prefixed with the current release slug until a non-matching heading
    is encountered. Supported change groups are `Added`, `Changed`,
    `Deprecated`, `Removed`, `Fixed`, and `Security`.
    """

    def __init__(self) -> None:
        """Initialize the slugifier."""
        self.release_slug: str | None = None

    def __call__(self, value: str, separator: str = "-") -> str:
        """Slugify a heading.

        Parameters:
            value: The heading text.
            separator: The separator used in the generated slug.

        Returns:
            The generated slug.
        """
        text = value.strip()

        match = _RELEASE_PATTERN.match(text)
        if match and (version := match.group("version")):
            version_slug = re.sub(r"[.+]", separator, version.lower())
            self.release_slug = f"v{version_slug}"
            return self.release_slug

        slug = default_slugify(text, separator)
        if self.release_slug and text.lower() in _CHANGE_GROUPS:
            return f"{self.release_slug}{separator}{slug}"

        self.release_slug = None
        return slug


slugify = Slugifier()
