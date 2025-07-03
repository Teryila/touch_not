#!/data/data/com.termux/files/usr/bin/bash

echo "[touch_not] Starting HackRF BTS..."
cd /data/data/com.termux/files/home/hackrf
# Simulated or real command to start OpenBTS:
./openbts_simulator --freq 935e6 --gain 40 --target +2349099199440
