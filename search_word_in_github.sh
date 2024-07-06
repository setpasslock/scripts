#!/bin/bash
# need gh

while IFS= read -r domain
do
    echo "Search in Code for $domain: ";
    gh search code "$domain" --limit 30;
    echo "========================================";

    echo "Search in Commits for $domain: ";
    gh search commits "$domain" --limit 30;
    echo "========================================";

    echo "Search in Issues for $domain: ";
    gh search issues "$domain" --limit 30;
    echo "========================================";

    echo "Search in Pull Requests for $domain";
    gh search prs "$domain" --limit 30;
    echo "========================================";

    echo "Search in Repos for $domain: ";
    gh search repos "$domain" --limit 30;
    echo "========================================";

    sleep 10


done < $1
