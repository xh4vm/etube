#!/bin/bash

INDEXES=(
    $INDEX_MOVIES 
    $INDEX_GENRES 
    $INDEX_PERSONS
)

sleep 1

for INDEX in ${INDEXES[*]}
do
    if [ "$(curl -s -o /dev/null -w '%{http_code}' http://elasticsearch:9200/$INDEX)" == "200" ]; then
        echo "[+] Index '$INDEX' existing"
    else
        echo "[-] Index '$INDEX' not existing"
        echo "[-] Creating index '$INDEX' with map..."
        if [ "$(curl -s -o /dev/null -w '%{http_code}' -XPUT http://elasticsearch:9200/$INDEX -H 'Content-Type: application/json' -d @./elasticsearch/indices/$INDEX.json)" == "200" ]; then
            echo "[+] Successfull creating index '$INDEX'"
        else
            echo "[+] Fatal error: creating index '$INDEX'... Aborting"
        fi
    fi
done