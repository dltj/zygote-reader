# ZygoteReader

Combine `YAMLMetadataReader` and `JinjaMarkdownReader` in one Pelican Reader

## Installation

This plugin can be installed via:

    python -m pip install git+https://github.com/dltj/zygote-reader

This plugin is named `ZygoteReader` to appear near the end of the alphabet. 
In biology, a zygote forms when two gametes merge, symbolizing the union of separate elements into a single entity. 
This name reflects the combination of different readers into one cohesive process.

If you haven't added a PLUGINS setting to your Pelican settings file, the newly-installed plugin should be automatically detected and enabled. 
Otherwise, add zygote-reader to your existing PLUGINS list. For more information, see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

## Usage

This plugin operates without further configuration.
It is hardcoded to first run the `YAMLMetadataReader` reader, then take the content output of that and run it through the `JinjaMarkdownReader` reader.
This reader then returns the metadata from `YAMLMetadataReader` and the rendered output of `JinjaMarkdownReader`.
