#!/usr/bin/env bash
set -euo pipefail

# Try primary selection first, then fallback to clipboard.
# --no-newline avoids adding an extra trailing newline.
output=$(
  wl-paste --primary --no-newline 2>/dev/null || \
  wl-paste --no-newline 2>/dev/null || \
  { printf '%s\n' "No selection or clipboard content available" >&2; exit 1; }
)

# Run llm-snippets grammar check and copy result to clipboard.
result=$(llm-snippets --command=eng_check --text="$output")
printf '%s' "$result" | wl-copy

# Send notification based on result
if [ -n "$result" ]; then
  notify-send "LLM Snippets" "Success" --icon=dialog-information
else
  notify-send "LLM Snippets" "Error" --icon=dialog-error --urgency=critical
fi
