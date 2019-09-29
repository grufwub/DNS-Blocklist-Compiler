#!/bin/sh

BASE_URL='rlwpx.free.fr/WPFF'
TRACKERS="$BASE_URL/htrc.7z"
ADS="$BASE_URL/hpub.7z"
MALWARE="$BASE_URL/hrsk.7z"

ORIG=$(pwd)
TEMP=$(mktemp -d)
cd "$TEMP"

curl -fL "$TRACKERS" -o 'trackers.7z'
curl -fL "$ADS" -o 'ads.7z'
curl -fL "$MALWARE" -o 'malware.7z'

7z x 'trackers.7z'
7z x 'ads.7z'
7z x 'malware.7z'

mv Hosts.* "$ORIG"
cd "$ORIG"
rm -rf "$TEMP"
