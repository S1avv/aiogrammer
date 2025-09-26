#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not found in PATH. Please install Python 3.12+." >&2
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  echo "pipx not found, installing with pip to user site-packages..."
  python3 -m pip install --user --upgrade pipx
fi

if command -v pipx >/dev/null 2>&1; then
  PIPX_CMD="pipx"
else
  PIPX_CMD="python3 -m pipx"
fi

$PIPX_CMD install --force .

if aiogrammer --help; then
  exit 0
else
  echo "aiogrammer is not on PATH yet. Attempting to run 'pipx ensurepath'..."
  $PIPX_CMD ensurepath || true
  echo "Please open a new terminal session and run: aiogrammer --help"
fi