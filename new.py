#! /usr/bin/env python3
from datetime import datetime
from os import getcwd
from sys import argv

day = datetime.now().isoformat().split("T")[0]
slug = argv[1]

stub = """---
title: TITLE HERE
---

Write markdown here!
"""

with open(f"{getcwd()}/src/posts/{day}-{slug}.md", "w") as f:
  f.write(stub)