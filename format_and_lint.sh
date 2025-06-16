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

echo "bandit code security check..."

# bandit -r . -x venv,*/migrations

# bandit -r . -x ./venv/,.*/migrations/,./.git

bandit -r . -x ./venv,./backend/migrations,./.git




