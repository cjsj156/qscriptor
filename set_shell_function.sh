#!/bin/bash

# Definition of qscriptor
qscriptor_function='
function qscriptor() {
    if [ $# -lt 1 ]; then
        echo "Usage: job_script_manager <project_path> [args...]"
        return 1
    fi

    cd "$1"
    local project_path="$(pwd -P)"
    local script="$project_path/qscriptor/script.py"

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
if grep -q "function qscriptor()" "$BASHRC_FILE"; then
    echo "[✔] 'qscriptor' already exists in .bashrc"
else
    echo "[+] Adding 'qscriptor' to $BASHRC_FILE"
    echo "$qscriptor_function" >> "$BASHRC_FILE"
    echo "[✔] Done. Run 'source ~/.bashrc' or restart your shell."
fi


