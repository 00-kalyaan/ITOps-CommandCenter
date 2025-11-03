#!/usr/bin/env bash
set -euo pipefail
find /tmp -type f -mtime +2 -print -delete
echo "Old /tmp files removed"
