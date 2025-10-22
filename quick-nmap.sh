#!/bin/bash
read -p "Enter target IP or host: " target
nmap -sC -sV -T4 -A -oN nmap_$target.txt $target
