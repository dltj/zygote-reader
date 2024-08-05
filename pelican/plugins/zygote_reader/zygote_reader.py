"""Module combining YAMLMetadataReader and JinjaMarkdownReader in one Pelican Reader."""

import os
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Tuple

from pelican.plugins.jinja2content import JinjaMarkdownReader
from pelican.plugins.yaml_metadata import YAMLMetadataReader
from pelican.readers import BaseReader

from pelican import signals


class ZygoteReader(YAMLMetadataReader, JinjaMarkdownReader, BaseReader):
    """Combine YAMLMetadataReader and YAMLMetadataReader in one Pelican Reader.

    ZygoteReader is a custom Pelican reader that combines the functionality
    of YAML metadata processing and Jinja templating. This reader is designed
    to handle files with YAML front-matter metadata and Jinja templating within
    the content.

    The reader first processes the YAML metadata, extracting any defined metadata
    fields. It then processes the content using Jinja templating, allowing for
    dynamic content generation based on the metadata and template context.

    This combination enables a more powerful and flexible content workflow,
    allowing authors to define metadata and dynamic content within the same file.

    Example:
    -------
        title: My Article
        date: 2023-10-05
        tags: [Python, Pelican]
        ---

        {% if some_condition %}
        This is a conditional content block.
        {% endif %}

    """

    enabled = True  # Ensure the reader is enabled

    def __init__(self, *args, **kwargs):
        """Pass through arguments to parents."""
        super().__init__(*args, **kwargs)

    def read(self, source_path: str) -> Tuple[Dict[str, Any], str]:
        """Process the input file to extract YAML metadata and render Jinja templates.

        Args:
        ----
            source_path (str): The file path of the source file to be read.

        Returns:
        -------
            Tuple[Dict[str, Any], str]: A tuple containing the metadata dictionary
                and the rendered content string.

        """
        # Process the YAML metadata part first
        content, metadata = YAMLMetadataReader.read(self, source_path)

        content = f"Title: Discarded Title\n\n{content}"

        # Process the Jinja content part
        with NamedTemporaryFile(delete=False) as f:
            f.write(content.encode())
            f.close()
            content, _ = JinjaMarkdownReader.read(self, f.name)
            os.unlink(f.name)

        return content, metadata


def add_reader(readers) -> None:
    """Register the custom ZygoteReader for specific file extensions.

    Args:
    ----
        readers (Readers): Pelican Readers instance to which the custom reader is added.

    """
    # Register the custom reader for specific file extensions, e.g., .md
    for ext in YAMLMetadataReader.file_extensions:
        readers.reader_classes[ext] = ZygoteReader


def register() -> None:
    """Connect the add_reader function to the Pelican readers_init signal."""
    signals.readers_init.connect(add_reader)
