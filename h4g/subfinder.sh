#!/bin/bash
read -p "Enter target IP or Domain: " domain
subfinder -d $domain -o subs.txt && httpx -l subs.txt -mc 200
