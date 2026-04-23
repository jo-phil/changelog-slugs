# changelog-slugs

[![CI](https://github.com/jo-phil/changelog-slugs/actions/workflows/ci.yml/badge.svg)](https://github.com/jo-phil/changelog-slugs/actions/workflows/ci.yml "View workflow runs")
[![PyPI - Version](https://img.shields.io/pypi/v/changelog-slugs)](https://pypi.org/project/changelog-slugs/ "View latest release on PyPI")
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/changelog-slugs)](https://pypi.org/project/changelog-slugs/ "View supported Python versions on PyPI")

`changelog-slugs` provides changelog-aware heading slugs for
[Python-Markdown](https://python-markdown.github.io/)’s
[`toc` extension](https://python-markdown.github.io/extensions/toc/).

It is designed for [Keep a Changelog](https://keepachangelog.com) style
changelogs in projects following [Semantic Versioning](https://semver.org),
where repeated subsection headings like `Added` and `Fixed` would otherwise
receive unstable, order-dependent anchors. As new releases are added above
older ones, those anchors can change, causing existing permalinks to become
obsolete. `changelog-slugs` instead scopes subsection slugs to their
containing release, producing stable anchors such as `v1-2-3-fixed`.

## Installation

```bash
pip install changelog-slugs
```

## Usage

**Python**

```python
import markdown

from changelog_slugs import Slugifier

changelog = ...  # e.g., the contents of your changelog file

html = markdown.markdown(
    changelog,
    extensions=["toc"],
    extension_configs={
        "toc": {
            "slugify": Slugifier(),
        },
    },
)
```

**zensical.toml**

```toml
[project.markdown_extensions.toc.slugify]
object = "changelog_slugs.Slugifier"
```

**mkdocs.yml**

```yaml
markdown_extensions:
  - toc:
      slugify: !!python/name:changelog_slugs.slugify
```

## License

This project is licensed under the terms of the MIT license.
