from contextlib import chdir

import markdown
import pytest
import zensical
from bs4 import BeautifulSoup
from mkdocs.commands.build import build
from mkdocs.config import load_config

from changelog_slugs import Slugifier

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

MKDOCS_CONFIG = """
site_name: MkDocs integration test

markdown_extensions:
  - toc:
      permalink: true
      slugify: !!python/name:changelog_slugs.slugify
"""

ZENSICAL_CONFIG = """
[project]
site_name = "Zensical integration test"

[project.markdown_extensions.toc]
permalink = true
slugify.object = "changelog_slugs.Slugifier"
"""


@pytest.fixture
def project_dir(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text(CHANGELOG)
    return tmp_path


def check_slugs(container):
    headings = container.find_all(["h1", "h2", "h3"])

    for heading, expected in zip(headings, EXPECTED_SLUGS, strict=True):
        assert heading.get("id") == expected
        permalink = heading.find("a", class_="headerlink").get("href")
        assert permalink == f"#{expected}"


def test_markdown_toc_integration():
    html = markdown.markdown(
        CHANGELOG,
        extensions=["toc"],
        extension_configs={"toc": {"permalink": True, "slugify": Slugifier()}},
    )
    check_slugs(BeautifulSoup(html, "html.parser"))


def test_mkdocs_integration(project_dir):
    (project_dir / "mkdocs.yml").write_text(MKDOCS_CONFIG)

    with chdir(project_dir):
        build(load_config())

    html = (project_dir / "site" / "index.html").read_text()
    soup = BeautifulSoup(html, "html.parser")

    check_slugs(soup.find(role="main"))


def test_zensical_integration(project_dir):
    (project_dir / "zensical.toml").write_text(ZENSICAL_CONFIG)

    with chdir(project_dir):
        zensical.build("zensical.toml", clean=True)

    html = (project_dir / "site" / "index.html").read_text()
    soup = BeautifulSoup(html, "html.parser")

    check_slugs(soup.find("article"))
