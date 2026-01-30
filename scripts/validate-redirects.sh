#!/bin/bash

# Validate GitBook redirects - checks that all destination files exist
# Usage: ./scripts/validate-redirects.sh

DOCS_ROOT="/Users/rachaelrenk/Documents/Warp/gitbook/docs"
GITBOOK_YAML="/Users/rachaelrenk/Documents/Warp/gitbook/.gitbook.yaml"

echo "Validating redirects in .gitbook.yaml..."
echo "Docs root: $DOCS_ROOT"
echo ""

# Extract redirects section and validate each destination
errors=0
checked=0

# Parse the redirects from .gitbook.yaml
# Format: "    old-path: new-path.md"
grep -E '^\s+[a-zA-Z0-9].*:' "$GITBOOK_YAML" | while read -r line; do
    # Skip comments and non-redirect lines
    if [[ "$line" =~ ^[[:space:]]*# ]] || [[ "$line" =~ ^root: ]]; then
        continue
    fi
    
    # Extract the destination (after the colon)
    destination=$(echo "$line" | sed 's/.*:[[:space:]]*//' | tr -d ' ')
    
    # Skip empty destinations
    if [[ -z "$destination" ]]; then
        continue
    fi
    
    # Check if destination file exists
    full_path="$DOCS_ROOT/$destination"
    
    ((checked++))
    
    if [[ ! -f "$full_path" ]]; then
        echo "❌ BROKEN: $destination"
        echo "   File not found: $full_path"
        ((errors++))
    fi
done

echo ""
echo "Checked redirect destinations."
echo "Run with verbose flag to see all checked paths."
