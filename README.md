# marcinfo2rss
A helper script to make marc.info archive into a RSS feed

## Background

OpenBSD has great mailing lists, archives of which is hosted in [marc.info](https://marc.info).
This script allows you to get the archives as a RSS feed to be added in newsboat.

## Installation

1. Copy `marc2rss.py` to `~/.config/newsboat`
1. Copy the marc2rss.sh to `$PATH`
2. Add the following line to newsboat's config: ```
filter:marc2rss.sh:https://marc.info/?l=openbsd-announce "~OpenBSD Announcements"
```

Only dependency to this is a Python 3 environment, it uses only standard library.
