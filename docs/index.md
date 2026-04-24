---
title: ""
icon: lucide/house
---

# changelog-slugs

--8<-- "README.md:opener"

## Installation

=== "pip"

    ```bash
    pip install changelog-slugs
    ```

=== "uv"

    ```bash
    uv add changelog-slugs
    ```

## Usage

=== "Python"

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

=== "zensical.toml"

    ```toml
    [project.markdown_extensions.toc.slugify]
    object = "changelog_slugs.Slugifier"
    ```

=== "mkdocs.yml"

    ```yaml
    markdown_extensions:
      - toc:
          slugify: !!python/name:changelog_slugs.slugify
    ```
