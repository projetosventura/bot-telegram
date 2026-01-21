#!/bin/bash

# Inicia o webhook em background
gunicorn -w 2 -b 0.0.0.0:$PORT webhook:app &

# Inicia o bot
python bot.py
