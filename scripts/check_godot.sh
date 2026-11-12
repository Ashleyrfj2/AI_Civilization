#!/bin/bash
# Real headless Godot startup check for the Phase 0 skeleton scene.
# - If no Godot binary is available, reports SKIP (skeleton preserved, untested).
# - Otherwise opens the project headless and runs the main scene briefly.
set -e
GODOT_BIN="${GODOT_BIN:-godot}"
if ! command -v "$GODOT_BIN" >/dev/null 2>&1; then
  echo "SKIP: Godot binary '$GODOT_BIN' not found; skeleton preserved, startup not tested."
  echo "      Install Godot 4.6 and re-run: bash scripts/check_godot.sh"
  exit 0
fi
"$GODOT_BIN" --version
"$GODOT_BIN" --headless --path godot --quit-after 1
echo "GODOT OK: project opened headless and main scene ran."
