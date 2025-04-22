#!/bin/bash

# Activate the virtual environment (if available)
if [ -d "/home/lubuntu/myenv" ]; then
    source /home/lubuntu/myenv/bin/activate
fi

# Install required packages if not already installed
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
