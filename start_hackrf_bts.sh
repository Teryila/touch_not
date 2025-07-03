#!/data/data/com.termux/files/usr/bin/bash

echo "[HackRF] Starting GSM BTS Simulation..."

# Example frequency: 935MHz (modify as needed)
grgsm_livemon -f 935e6 -g 40 > bts.log 2>&1
