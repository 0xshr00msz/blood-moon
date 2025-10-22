#!/bin/bash

# -----------------------------------------------
# AUTO-RECON SUITE
# Runs Gobuster, IDOR-Forge, Nmap, and Subfinder
# concurrently for faster reconnaissance
# -----------------------------------------------

# Paths (adjust if necessary)
IDOR_PATH="$HOME/IDOR-Forge"
WORDLIST="/usr/share/wordlists/SecLists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt"

# Timestamp for output organization
timestamp=$(date +"%Y%m%d_%H%M%S")
mkdir -p results_${timestamp}
cd results_${timestamp} || exit 1

echo "=========================================="
echo "        AUTO RECON by 0xshr00msz"
echo "=========================================="
echo

# Ask for base target inputs
read -p "Enter target domain or IP (e.g., example.com or 10.10.10.10): " target

if [ -z "$target" ]; then
  echo "[-] No target entered. Exiting."
  exit 1
fi

read -p "Enter full URL for web-based scans (e.g., https://example.com): " url

if [ -z "$url" ]; then
  echo "[-] No URL entered. Exiting."
  exit 1
fi

echo "[+] Starting all scans asynchronously..."
echo

# ------------------- NMAP -------------------
(
  echo "[Nmap] Starting scan..."
  nmap -sC -sV -T4 -A -oN nmap_$target.txt $target
  echo "[Nmap] Scan finished -> nmap_$target.txt"
) &

# ------------------- GOBUSTER -------------------
(
  echo "[Gobuster] Starting enumeration..."
  gobuster dir -u "$url" -w "$WORDLIST" -o gobuster_$target.txt
  echo "[Gobuster] Enumeration finished -> gobuster_$target.txt"
) &

# ------------------- SUBFINDER -------------------
(
  echo "[Subfinder] Enumerating subdomains..."
  subfinder -d "$target" -o subs_$target.txt
  echo "[Subfinder] Checking live subdomains with httpx..."
  httpx -l subs_$target.txt -mc 200 -o live_subs_$target.txt
  echo "[Subfinder] Finished -> subs_$target.txt, live_subs_$target.txt"
) &

# ------------------- IDOR-FORGE -------------------
(
  if [ -f "$IDOR_PATH/idorforge.py" ]; then
    echo "[IDOR-Forge] Testing for IDOR vulnerabilities..."
    cd "$IDOR_PATH" || exit 1
    python3 idorforge.py -u "$url" > "$OLDPWD/idorforge_$target.txt"
    echo "[IDOR-Forge] Finished -> idorforge_$target.txt"
  else
    echo "[-] IDOR-Forge not found at $IDOR_PATH — skipping."
  fi
) &

# ------------------- Wait for completion -------------------
wait

echo
echo "=========================================="
echo "        All scans completed!"
echo "        Results saved in: $(pwd)"
echo "=========================================="

