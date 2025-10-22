#!/bin/bash

# Ask for the target URL
read -p "Enter the target URL (e.g., http://example.com): " url

# Check if input is empty
if [ -z "$url" ]; then
    echo "Error: No URL provided. Exiting."
    exit 1
fi

# Run Gobuster with hardcoded parameters
gobuster dir -u "$url" -w /usr/share/wordlists/SecLists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt

