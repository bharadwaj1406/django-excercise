#! /bin/bash


#################################
# This script formats and lints the code in the current directory.
#################################

set -x

pwd

echo "Formatting and linting code..."
# Format the code using black
black .

# Lint the code using flake8
flake8 .

