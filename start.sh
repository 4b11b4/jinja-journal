#!/bin/bash

# Colors for prettier output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Jinja Journal...${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
pip install -r requirements.txt

# Run the application
echo -e "${GREEN}Running Jinja Journal...${NC}"
python app.py

# Deactivate virtual environment
deactivate 