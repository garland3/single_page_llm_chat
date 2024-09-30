#!/bin/bash

# Define file paths
INPUT_FILE="index_dev.html"
OUTPUT_FILE="index.html"
JS_FILE="marked.min.js"

# Check if input files exist
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: Input file '$INPUT_FILE' does not exist."
    exit 1
fi

if [[ ! -f "$JS_FILE" ]]; then
    echo "Error: JavaScript file '$JS_FILE' does not exist."
    exit 1
fi

# Read the JavaScript content
JS_CONTENT=$(cat "$JS_FILE")

# Use awk to replace the script tag with inlined JavaScript
awk -v js="$JS_CONTENT" '
    /<script src="marked\.min\.js"><\/script>/ {
        print "<script>"
        print js
        print "</script>"
        next
    }
    { print }
' "$INPUT_FILE" > "$OUTPUT_FILE"

# Verify if the awk command was successful
if [[ $? -eq 0 ]]; then
    echo "Success: Updated HTML file saved to '$OUTPUT_FILE'."
else
    echo "Error: Failed to update the HTML file."
    exit 1
fi
