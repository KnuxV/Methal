#!/usr/bin/env bash

# "Convert asciidoc to Github Flavored Markdown · GitHub"
# From https://gist.github.com/cheungnj/38becf045654119f96c87db829f1be8e

# The GitLab project wiki uses asciidoc. This script is in case we need to mirror
# the wiki to GitHub

# Adapted from https://tinyapps.org/blog/nix/201701240700_convert_asciidoc_to_markdown.html
# Using asciidoctor 1.5.6.1 and pandoc 2.0.0.1
# Install pandoc and asciidoctor

#sudo apt install asciidoctor
#sudo wget https://github.com/jgm/pandoc/releases/download/2.0.0.1/pandoc-2.0.0.1-1-amd64.deb
#sudo dpkg -i pandoc-2.0.0.1-1-amd64.deb


# Convert asciidoc to docbook using asciidoctor

asciidoctor -b docbook foo.adoc

# foo.xml will be output into the same directory as foo.adoc

# Convert docbook to markdown

pandoc -f docbook -t gfm foo.xml -o foo.md

# Unicode symbols were mangled in foo.md. Quick workaround:

iconv -t utf-8 foo.xml | pandoc -f docbook -t gfm | iconv -f utf-8 > foo.md

# Pandoc inserted hard line breaks at 72 characters. Removed like so:

pandoc -f docbook -t gfm --wrap=none # don't wrap lines at all

pandoc -f docbook -t gfm --columns=120 # extend line breaks to 120
