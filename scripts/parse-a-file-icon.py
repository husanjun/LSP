#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A script to parse the additional base scopes created by the "A File Icon" package.
# The script:
# - downloads the icon/icons.js file from the master branch of github.com/deathaxe/AFileIcon
# - parses the language-ids.sublime-settings map
# - compares the icons file with the language-ids.sublime-setings map and
#   prints out the most likely language ID
from typing import Dict
import jsmin  # pip3 install jsmin
import json
import os
import re
import sys
import urllib.request

URL = "https://raw.githubusercontent.com/SublimeText/AFileIcon/master/icons/icons.json"
FILE_TYPE_PREFIX = "file_type_"

def main():
    with urllib.request.urlopen(URL) as fp:
        content = fp.read()
    icons = json.loads(content)
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "language-ids.sublime-settings")
    with open(path, "r") as fp:
        content = jsmin.jsmin(fp.read())
    content = re.sub(",}$","}", content)  # remove trailing comma
    language_id_map = json.loads(content)
    candidates: Dict[str, str] = {}
    for v in icons.values():
        aliases = v.get("aliases")
        if not aliases:
            continue
        for alias in aliases:
            base = alias.get("base")
            if not base:
                continue
            scope = alias.get("scope")
            if not scope:
                continue
            if scope in language_id_map:
                print(scope, "already in language ID map, skipping", file=sys.stderr)
                continue
            candidates[scope] = language_id_map.get(base) or base.split(".")[-1]
    print()
    print("The following scopes should be added:")
    json.dump(candidates, sys.stdout, indent=4, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
