#!/bin/bash

if [ "$(curl -s -o /dev/null -w '%{http_code}' http://elasticsearch:9200/$INDEX_MOVIES)" == "200" ]; then  
    echo "[+] Index '$INDEX_MOVIES' existing"
else
    echo "[-] Index '$INDEX_MOVIES' not existing"
    echo "[-] Creating index '$INDEX_MOVIES' with map..."
    if [ "$(curl -s -o /dev/null -w '%{http_code}' -XPUT http://elasticsearch:9200/$INDEX_MOVIES -H 'Content-Type: application/json' -d @./elasticsearch/indices/$INDEX_MOVIES.json)" == "200" ]; then  
        echo "[+] Successfull creating index '$INDEX_MOVIES'"
    else
        echo "[+] Fatal error: creating index '$INDEX_MOVIES'... Aborting"
    fi
fi
