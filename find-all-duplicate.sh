#!/bin/bash
#usage: ./find-all-duplicate.sh "/search/path"



declare -A file_hashes


calculate_hashes() {
    local dir="$1"
    local files=()
    mapfile -t files < <(find "$dir" -type f)
    for file in "${files[@]}"; do
        hash=$(md5sum "$file" | awk '{print $1}')
        file_hashes["$hash"]+=" $file"
    done
}


calculate_hashes $1


for hash in "${!file_hashes[@]}"; do
    files=(${file_hashes["$hash"]})
    if [ ${#files[@]} -gt 1 ]; then
	echo -e "\e[31m-------------------------------------------------------------------------------\e[0m"
        echo "Duplicate md5 hash: $hash"
        for file in "${files[@]}"; do
            echo "  $file"
        done
        echo -e "\e[31m-------------------------------------------------------------------------------\e[0m"
    fi
done
