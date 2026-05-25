#!/bin/bash
set -o errexit

# Instalar dependências do sistema para discord.py
apt-get update
apt-get install -y libopus0 libopus-dev ffmpeg

# Instalar pacotes Python
pip install --upgrade pip
pip install -r requirements.txt
