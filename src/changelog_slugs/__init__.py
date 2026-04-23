"""Changelog-aware heading slugs for Python-Markdown."""

__all__ = ["DEFAULT_SECTIONS", "Slugifier", "slugify"]

import re
from collections.abc import Collection

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

DEFAULT_SECTIONS = frozenset(
    {
        "Added",
        "Changed",
        "Deprecated",
        "Removed",
        "Fixed",
        "Security",
    }
)
"""Default sections following the Keep a Changelog format."""


class Slugifier:
    """Slugifier for changelog headings with release-scoped subsections.

    It recognizes release headings that begin with a version following
    [SemVer](https://semver.org), optionally prefixed with `v`. For example,
    `[0.1.0] - 2026-04-11`, `0.1.0 some text`, and `v0.1.0` all resolve
    to the release slug `v0-1-0`.

    Subsequent headings matching the configured `sections` are prefixed
    with the current release slug until a non-matching heading is
    encountered. The default sections are based on Keep a Changelog.
    """

    def __init__(self, sections: Collection[str] = DEFAULT_SECTIONS) -> None:
        """Initialize the slugifier.

        Parameters:
            sections: Sections to recognize after a release heading.
                Set this when your changelog uses headings such as
                `Enhancements` or `Bug fixes` instead of the default
                Keep a Changelog change types.
        """
        self.release_slug: str | None = None

        self.sections = frozenset(section.lower() for section in sections)

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
        if self.release_slug and text.lower() in self.sections:
            return f"{self.release_slug}{separator}{slug}"

        self.release_slug = None
        return slug


slugify = Slugifier()
"""Default slugifier instance."""
