#!/bin/bash

# Usage: ./nmap-scan.sh <TARGET_IP>

if [ -z "$1" ]; then
    echo "Usage: $0 <TARGET_IP>"
    exit 1
fi

TARGET=$1
DATE=$(date +%Y-%m-%d_%H-%M-%S)
OUTDIR="nmap-$TARGET-$DATE"

mkdir -p "$OUTDIR"

echo "[*] Scanning all TCP ports on $TARGET..."
nmap -p- -T4 -vv "$TARGET" -oN "$OUTDIR/nmap-allports.txt" --stats-every 1s

echo "[*] Running detailed scan on open ports..."
OPEN_PORTS=$(grep -oP '^\d+/tcp' "$OUTDIR/nmap-allports.txt" | cut -d/ -f1 | paste -sd, -)

if [ -n "$OPEN_PORTS" ]; then
    nmap -sC -sV -vv -p "$OPEN_PORTS" "$TARGET" --stats-every 1s -oN "$OUTDIR/nmap-services.txt"
else
    echo "[-] No open ports found."
fi

echo "[+] Nmap scan complete. Output saved to $OUTDIR/"

