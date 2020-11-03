#/bin/sh

# let read split lines at \n only
IFS=$'\n'

while read line; do
    n=$(echo "$line" | cut -f 1)
    id=$(echo "$line" | cut -f 2)

    if [ -z "$id" ]; then
        continue
    fi

    python3 position_to_font.py "$id" --prefix="$n" --output=png --mirror

done <input/bill_robertie_501_essential_backgammon_problems/positions.txt
