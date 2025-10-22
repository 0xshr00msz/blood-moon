#!/bin/bash

# IDOR detector script using IDOR-Forge

# Change IDOR-Forge path
IDOR_PATH="$HOME/IDOR-Forge"

# Check if tool exists
if [ ! -f "$IDOR_PATH/idorforge.py" ]; then
  echo "[-] IDOR-Forge not found at $IDOR_PATH"
  exit 1
fi

# Ask for target URL
read -p "Enter the target URL (e.g., https://example.com/profile?id=1): " url

if [ -z "$url" ]; then
  echo "[-] No URL provided. Exiting."
  exit 1
fi

# Run IDOR-Forge
cd "$IDOR_PATH" || exit 1
python3 idorforge.py -u "$url"
