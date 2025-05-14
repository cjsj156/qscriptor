#!/bin/bash

# Definition of qscriptor
qscriptor_function='
function runsync_script() {
    if [ $# -lt 1 ]; then
        echo "Usage: runsync_script <project_path> [args...]"
        return 1
    fi

    cd "$1"
    local project_path="$(pwd -P)"
    local script="$project_path/runsync/script.py"

    if [ ! -f "$script" ]; then
        echo "Error: script.py not found at $script"
        return 1
    fi

    local lines

    project_path="$(pwd -P)"
    shift
    output="$(python "$script" "$project_path" "$@")"

    readarray -t lines <<< "$output"
    if (( ${#lines[@]} >= 3 )); then
        echo "${arr[@]}"
    fi

    cd "${lines[0]}"
    echo "${lines[1]}"
}
'

BASHRC_FILE="$HOME/.bashrc"

# check if qscriptor already exists
if grep -q "function runsync_script()" "$BASHRC_FILE"; then
    echo "[✔] 'runsync_script' already exists in .bashrc"
else
    echo "[+] Adding 'runsync_script' to $BASHRC_FILE"
    echo "$qscriptor_function" >> "$BASHRC_FILE"
    echo "[✔] Done. Run 'source ~/.bashrc' or restart your shell."
fi


