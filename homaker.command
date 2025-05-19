#!/bin/bash

# homaker.command - Run homaker on the current directory
# This script will run homaker on the directory where it's executed from

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the directory where the script is located
cd "$SCRIPT_DIR"

# Display startup message
echo "Running homaker in: $(pwd)"
echo "Looking for worksheets to convert to handouts..."

# Run homaker
homaker

# Check if command was successful
if [ $? -eq 0 ]; then
    echo "✅ homaker completed successfully."
    echo "All worksheets have been converted to handouts."
else
    echo "❌ Error: homaker encountered a problem."
    echo "See above messages for details."
fi

# Keep terminal window open for a few seconds before closing
echo ""
echo "This window will close automatically in 5 seconds..."
sleep 5