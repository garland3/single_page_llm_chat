#!/usr/bin/env python3

import os
import sys
import re
import shutil

def error_exit(message):
    """Prints an error message and exits the script."""
    print(f"Error: {message}")
    sys.exit(1)

def read_file(filepath):
    """Reads the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        error_exit(f"Unable to read file '{filepath}': {e}")

def write_file(filepath, content):
    """Writes content to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        error_exit(f"Unable to write to file '{filepath}': {e}")

def inline_js(input_html, js_content, js_filename):
    """
    Replaces the <script src="js_filename"></script> tag in input_html with
    <script>js_content</script>.
    """
    # Compile a regex pattern to find the exact script tag
    # The pattern is case-insensitive and allows for arbitrary whitespace
    pattern = re.compile(
        r'<script\s+src=[\'"]' + re.escape(js_filename) + r'[\'"]\s*>\s*</script>',
        re.IGNORECASE
    )
    
    # Replacement string: inlined JavaScript without line breaks
    replacement = f'<script>{js_content}</script>'
    
    # To safely handle special characters in the replacement string,
    # use a lambda function to return the replacement as a literal string
    new_html, count = pattern.subn(lambda _: replacement, input_html)
    
    if count == 0:
        error_exit(f'<script src="{js_filename}"></script> not found in the HTML file.')
    
    return new_html

def main():
    # Define file paths
    INPUT_FILE = "index_dev.html"
    OUTPUT_FILE = "index.html"
    JS_FILE = "marked.min.js"
    BACKUP_FILE = "index_dev_backup.html"
    
    # Check if input files exist
    if not os.path.exists(INPUT_FILE):
        error_exit(f"Input file '{INPUT_FILE}' does not exist.")
    if not os.path.exists(JS_FILE):
        error_exit(f"JavaScript file '{JS_FILE}' does not exist.")
    
    # Create a backup of the original HTML file
#    if not os.path.exists(BACKUP_FILE):
#        try:
#            shutil.copyfile(INPUT_FILE, BACKUP_FILE)
#            print(f"Backup created: '{BACKUP_FILE}'")
#        except Exception as e:
#            error_exit(f"Unable to create backup of '{INPUT_FILE}': {e}")
#    else:
#        print(f"Backup already exists: '{BACKUP_FILE}'")
#    
    # Read the contents of the JavaScript file as a single line
    js_raw_content = read_file(JS_FILE)
    js_single_line = js_raw_content.replace('\n', '').replace('\r', '').strip()
    
    # Read the contents of the original HTML file from the backup
    html_content = read_file(INPUT_FILE)
    
    # Inline the JavaScript into the HTML content
    updated_html = inline_js(html_content, js_single_line, JS_FILE)
    
    # Write the updated HTML to the output file
    write_file(OUTPUT_FILE, updated_html)
    
    print(f"Success: Updated HTML file saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
