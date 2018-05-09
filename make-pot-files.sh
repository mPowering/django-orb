#!/usr/bin/env bash

# Bash script that renders pot (template, source) gettext files from po files
# which may contain translations.
#
# The empty pot translation files are required for some services, e.g. Transifex.

find orb -name "*.po" -print0 | xargs -0 -I {} msgfilter -i {} -o {}.pot true
