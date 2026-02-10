#!/usr/bin/env bash
set -euo pipefail

# Try primary selection first, then fallback to clipboard.
# --no-newline avoids adding an extra trailing newline.
output=$(
  wl-paste --primary --no-newline 2>/dev/null || \
  wl-paste --no-newline 2>/dev/null || \
  { printf '%s\n' "No selection or clipboard content available" >&2; exit 1; }
)

# Convert to uppercase and copy to clipboard (regular clipboard).
# Preserve content exactly except for case change.
printf '%s' "$output" | tr '[:lower:]' '[:upper:]' | wl-copy

#send system notification
# TODO