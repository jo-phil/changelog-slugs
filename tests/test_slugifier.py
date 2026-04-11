import pytest
from markdown.extensions.toc import slugify as default_slugify

from changelog_slugs import Slugifier

# Valid and invalid SemVer versions from https://regex101.com/r/vkijKf/1/
# without invalid `1.0.0-alpha_beta`, as trailing text (`_beta`) is allowed
VALID_VERSIONS = ["0.0.4", "1.2.3", "10.20.30", "1.1.2-prerelease+meta", "1.1.2+meta", "1.1.2+meta-valid", "1.0.0-alpha", "1.0.0-beta", "1.0.0-alpha.beta", "1.0.0-alpha.beta.1", "1.0.0-alpha.1", "1.0.0-alpha0.valid", "1.0.0-alpha.0valid", "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay", "1.0.0-rc.1+build.1", "2.0.0-rc.1+build.123", "1.2.3-beta", "10.2.3-DEV-SNAPSHOT", "1.2.3-SNAPSHOT-123", "1.0.0", "2.0.0", "1.1.7", "2.0.0+build.1848", "2.0.1-alpha.1227", "1.0.0-alpha+beta", "1.2.3----RC-SNAPSHOT.12.9.1--.12+788", "1.2.3----R-S.12.9.1--.12+meta", "1.2.3----RC-SNAPSHOT.12.9.1--.12", "1.0.0+0.build.1-rc.10000aaa-kk-0.1", "99999999999999999999999.999999999999999999.99999999999999999", "1.0.0-0A.is.legal"]  # fmt: skip
INVALID_VERSIONS = ["1", "1.2", "1.2.3-0123", "1.2.3-0123.0123", "1.1.2+.123", "+invalid", "-invalid", "-invalid+invalid", "-invalid.01", "alpha", "alpha.beta", "alpha.beta.1", "alpha.1", "alpha+beta", "alpha_beta", "alpha.", "alpha..", "beta", "-alpha.", "1.0.0-alpha..", "1.0.0-alpha..1", "1.0.0-alpha...1", "1.0.0-alpha....1", "1.0.0-alpha.....1", "1.0.0-alpha......1", "1.0.0-alpha.......1", "01.1.1", "1.01.1", "1.1.01", "1.2", "1.2.3.DEV", "1.2-SNAPSHOT", "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788", "1.2-RC-SNAPSHOT", "-1.0.3-gamma+b7718", "+justmeta", "9.8.7+meta+meta", "9.8.7-whatever+meta+meta", "99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1--------------------------------..12"]  # fmt: skip

PREFIXES = [
    pytest.param("", id="no-prefix"),
    pytest.param("v", id="v-prefix"),
]

BRACKETS = [
    pytest.param(("", ""), id="no-brackets"),
    pytest.param(("[", "]"), id="brackets"),
]

SUFFIXES = [
    pytest.param("", id="no-suffix"),
    pytest.param(" - 2026-04-11", id="date"),
    pytest.param(": some text", id="colon-text"),
]


@pytest.fixture
def slugify():
    return Slugifier()


@pytest.mark.parametrize("suffix", SUFFIXES)
@pytest.mark.parametrize("brackets", BRACKETS)
@pytest.mark.parametrize("prefix", PREFIXES)
@pytest.mark.parametrize("version", VALID_VERSIONS)
def test_valid_release_heading(slugify, version, prefix, brackets, suffix):
    slug = slugify(f"{brackets[0]}{prefix}{version}{brackets[1]}{suffix}")
    expected = f"v{version.lower().replace('.', '-').replace('+', '-')}"
    assert slug == expected
    assert slugify.release_slug == expected


@pytest.mark.parametrize("suffix", SUFFIXES)
@pytest.mark.parametrize("brackets", BRACKETS)
@pytest.mark.parametrize("prefix", PREFIXES)
@pytest.mark.parametrize("version", INVALID_VERSIONS)
def test_invalid_version(slugify, version, prefix, brackets, suffix):
    text = f"{brackets[0]}{prefix}{version}{brackets[1]}{suffix}"
    slug = slugify(text)
    assert slug == default_slugify(text, separator="-")
    assert slugify.release_slug is None


def test_invalid_release_heading(slugify):
    text = "Python 3.14.4 support"
    slug = slugify(text)
    assert slug == default_slugify(text, separator="-")
    assert slugify.release_slug is None


def test_stateful_release_context(slugify):
    # Before the first release heading, change groups are not prefixed.
    assert slugify("Added") == "added"
    assert slugify.release_slug is None

    # A release heading sets the release context.
    assert slugify("1.0.0") == "v1-0-0"
    assert slugify.release_slug == "v1-0-0"

    # Matching change groups are prefixed with the current release slug.
    assert slugify("Added") == "v1-0-0-added"
    assert slugify("Changed") == "v1-0-0-changed"
    assert slugify.release_slug == "v1-0-0"

    # A non-matching heading resets the release context.
    assert slugify("Notes") == "notes"
    assert slugify.release_slug is None

    # After reset, change groups are no longer prefixed.
    assert slugify("Added") == "added"
    assert slugify.release_slug is None

    # A new release heading starts a new release context.
    assert slugify("0.1.0") == "v0-1-0"
    assert slugify.release_slug == "v0-1-0"

    # Matching change groups are now prefixed with the new release slug.
    assert slugify("Added") == "v0-1-0-added"
    assert slugify("Fixed") == "v0-1-0-fixed"
    assert slugify.release_slug == "v0-1-0"
